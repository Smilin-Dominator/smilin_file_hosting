/// <reference path="../declarations.d.ts" />
import {NextFunction, Request, Response} from "express";
import Redis from "../util/redis";

export const Authorization = async (req: Request, res: Response, next: NextFunction) => {
    const authHeader = req.header('Authorization');
    if (!authHeader) {
        res.status(401).json({
            success: false,
            error: "No authorization header"
        })
    } else {
        const token = authHeader.replace("Bearer ", "");
        const user_id = await Redis.getUserId(token);
        if (!user_id) {
            res.status(401).json({
                success: false,
                error: "Invalid access token!"
            })
        } else {
            req.user_id = user_id;
            next();
        }
    }
}
