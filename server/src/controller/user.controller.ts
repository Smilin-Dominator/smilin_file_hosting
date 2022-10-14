import {Request, Response} from "express";
import Cassandra from "../util/cassandra";
import {randomUUID} from "crypto";
import Redis from "../util/redis";

export namespace UserController {

    export const registerHandler = async (req: Request, res: Response) => {
        const user_id = randomUUID();
        await Cassandra.createUser(user_id); // create a user in the database
        const access_token = await Redis.createAccessToken(user_id); // generate the access token
        res.status(200).json({
            success: true,
            data: {
                user_id: user_id,
                access_token: access_token,
            }
        });
    }

    export const loginHandler = async (req: Request, res: Response) => {
        const user_id = req.user_id!;
        const access_token = await Redis.createAccessToken(user_id); // create a new access token
        res.status(200).json({
            success: true,
            data: {
                user_id: user_id,
                access_token: access_token,
            }
        });
    }

    export const deleteAccountHandler = async (req: Request, res: Response) => {
        const user_id = req.user_id!;
        await Cassandra.deleteUser(user_id);
        res.status(200).json({
            success: true,
            message: "Account deleted successfully!"
        })
    }

}
