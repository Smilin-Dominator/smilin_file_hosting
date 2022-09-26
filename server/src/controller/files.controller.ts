import {Request, Response} from "express";
import {types} from "cassandra-driver";
import Cassandra from "../util/cassandra";
import {createFileObject, File} from "../model/File";
import fs from "fs";
import path from "path";
import {Stream} from "stream";

export namespace FilesController {

    export const describeFileHandler = async (req: Request, res: Response) => {
        const user_id = types.Uuid.fromString(req.user_id!);
        const file_id = types.Uuid.fromString(req.file_id!);
        const file = await Cassandra.getFileInfo(user_id, file_id);
        res.status(200).json({
            success: true,
            data: file,
        });
    }

    export const deleteFileHandler = async (req: Request, res: Response) => {
        const user_id = types.Uuid.fromString(req.user_id!);
        const file_id = types.Uuid.fromString(req.file_id!);
        const stored_filename = await Cassandra.getStoredFilename(user_id, file_id);
        if (stored_filename == undefined) {
            res.status(400).json({
                success: false,
                error: "No such file exists!"
            });
        } else {
            const pathToFile = path.join('files', stored_filename);
            await Cassandra.deleteFileInfo(user_id, file_id);
            fs.rmSync(pathToFile);
            res.status(200).json({
                success: true
            });
        }
    }

    export const addFileHandler = async (req: Request, res: Response) => {

        const user_id = types.Uuid.fromString(req.user_id!);

        let iv: Buffer;
        let encrypted_filename: Buffer;
        let fileObject: File;

        req.busboy.on('field', (name: string, value: Buffer | Stream, _info: any) => {
            if (name == "iv") {
                iv = value as Buffer;
            }
            if (name == "encrypted_filename") {
                encrypted_filename = value as Buffer;
            }
        });

        req.busboy.on('file', async (fieldName: string, file: Stream, _fileInfo: any) => {
            if (fieldName == "file") {

                fileObject = createFileObject(user_id, iv, encrypted_filename);
                await Cassandra.addFileInfo(user_id, encrypted_filename, iv); // persist

                const filePath = path.join('files', fileObject.stored_filename);
                const writeStream = fs.createWriteStream(filePath);

                file.pipe(writeStream); // write the file to disk

            }
        });

        req.busboy.on('finish', () => {
            res.status(200).json({
                success: true,
                data: fileObject,
            })
        });

        req.pipe(req.busboy); // handle the request with busboy

    }

    export const updateFileHandler = async (req: Request, res: Response) => {

        const user_id = types.Uuid.fromString(req.user_id!);
        const file_id = types.Uuid.fromString(req.file_id!);

        let iv: Buffer;
        let encrypted_filename: Buffer;
        let fileObject: File;

        req.busboy.on('field', (name: string, value: Buffer | string, _info: any) => {
            if (name == "iv") {
                iv = value as Buffer;
            }
            if (name == "encrypted_filename") {
                encrypted_filename = value as Buffer;
            }
        });

        req.busboy.on('file', async (fieldName: string, file: Stream, _fileInfo: any) => {
            if (fieldName == "file") {

                const prevFilename = await Cassandra.getStoredFilename(user_id, file_id);
                const fileExists = prevFilename != undefined;
                fileObject = createFileObject(user_id, iv, encrypted_filename, file_id);

                if (fileExists) {
                    const prevPath = path.join('files', prevFilename);
                    fs.rmSync(prevPath);
                    await Cassandra.updateFileInfo(user_id, file_id, encrypted_filename, iv);
                } else {
                    await Cassandra.addFileInfo(user_id, encrypted_filename, iv);
                }

                const newPath = path.join('files', fileObject.stored_filename);
                const writeStream = fs.createWriteStream(newPath);

                file.pipe(writeStream); // write the file to disk

            }
        });

        req.busboy.on('finish', () => {
            res.status(200).json({
                success: true,
                data: fileObject,
            })
        });

        req.pipe(req.busboy); // handle the request with busboy

    }

}
