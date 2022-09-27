import {NextFunction, Request, Response} from "express";

export namespace FileID {

    export const QueryParams = async (req: Request, res: Response, next: NextFunction) => {
        const id = req.query.file_id;
        if (id == undefined) {
            res.status(400).json({
                success: false,
                error: "File ID wasn't defined"
            })
        } else {
            req.file_id = id as string;
            next();
        }
    }

}
