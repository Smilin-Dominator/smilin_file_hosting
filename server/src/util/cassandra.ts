import {Client, QueryOptions, types} from "cassandra-driver";
import {convertRowToFile, createFileObject, File} from "../model/File";

namespace Cassandra {

    let client: Client;
    let queryOpts: QueryOptions = {prepare: true};

    /**
     * This accepts a username, password and sets up a cassandra client
     * @param username The username
     * @param password The password
     * @param contact_points URLs of Cassandra nodes
     * @param datacenter The datacenter
     */
    export async function setup(username: string, password: string, contact_points: string[], datacenter?: string) {
        client = new Client({
            contactPoints: contact_points,
            localDataCenter: datacenter ?? "datacenter1",
            credentials: {
                username: username,
                password: password,
            }
        });
        await client.connect();
    }

    // User Functions

    /**
     * This creates a user in (app.users)
     * @param user_id The user id (UUID)
     */
    export async function createUser(user_id: string): Promise<void> {
        await client.execute(`
            INSERT INTO app.users (id) 
            VALUES (?)
        `, [user_id], queryOpts);
    }

    /**
     * This deletes a user from (app.users)
     * @param user_id The user id (UUID)
     */
    export async function deleteUser(user_id: string): Promise<void> {
        await client.execute(`
            DELETE FROM app.users 
            WHERE id = ?
        `, [user_id], queryOpts);
    }

    // Files

    /**
     * This accepts the user id and the file id and returns the file's ID, Encrypted Filename, Initialization Vector
     * and the date and time it was added
     * @param user_id The user's id
     * @param file_id The file's id
     * @return A file object that contains the ID, Encrypted Filename, Initialization Vector and the Date-Time it was
     * added
     */
    export async function getFileInfo(user_id: types.Uuid, file_id: types.Uuid): Promise<File> {
        const res = await client.execute(`
            SELECT id, encrypted_filename, iv, date_added 
            FROM app.files 
            WHERE uid = ? AND id = ?
            LIMIT 1
        `, [ user_id, file_id ], queryOpts);
        return convertRowToFile(res.first());
    }

    /**
     * This accepts the user id and file id and deletes the file data from the database
     * @param user_id The user's id
     * @param file_id The file's id
     */
    export async function deleteFileInfo(user_id: types.Uuid, file_id: types.Uuid): Promise<void> {
        await client.execute(`
            DELETE FROM app.files 
            WHERE uid = ? AND id = ?
        `, [ user_id, file_id ], queryOpts);
    }

    /**
     * This accepts the user id, file id, new encrypted filename and the new iv and updates the existing database
     * entry with the new values
     * @param user_id The user's id
     * @param file_id The file's id
     * @param filename The encrypted filename
     * @param iv The initialization vector used to encrypt the file and filename
     * @return The updated file object
     */
    export async function updateFileInfo(user_id: types.Uuid, file_id: types.Uuid, filename: Buffer, iv: Buffer): Promise<File> {
        const file: File = createFileObject(user_id, iv, filename, file_id);
        await client.execute(`
            UPDATE app.files
            SET
                encrypted_filename = ?,
                stored_filename = ?,
                iv = ?,
                date_added = ?
            WHERE uid = ? AND id = ?
        `, [ file.encrypted_filename, file.stored_filename, file.iv, file.date_added, file.uid, file.id ], queryOpts);
        return file;
    }

    /**
     * This accepts the user id, filename and the initialization vector and creates a new database entry
     * @param user_id The user's id
     * @param filename The encrypted filename
     * @param iv The initialization vector used to encrypt the file and filename
     * @return The new file object
     */
    export async function addFileInfo(user_id: types.Uuid, filename: Buffer, iv: Buffer): Promise<File> {
        const file: File = createFileObject(user_id, iv, filename);
        await client.execute(`
            INSERT INTO app.files (id, uid, encrypted_filename, iv, stored_filename, date_added)
            VALUES (?, ?, ? , ? , ? , ?)
        `, [ file.id, file.uid, file.encrypted_filename, file.iv, file.stored_filename, file.date_added ], queryOpts);
        return file;
    }

}

export default Cassandra;
