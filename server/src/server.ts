import Redis from "./util/redis";
import Cassandra from "./util/cassandra";
import express from "express";
import cors from "cors";
import busboy from "connect-busboy";
import UserRoutes from "./routes/user.routes";
import FilesRoutes from "./routes/files.routes";
import dotenv from "dotenv";

interface Environment {

    SMILIN_FILE_HOSTING_PORT: number; // The port the API should run on

    REDIS_URL: string; // The URL to the Redis DB
    REDIS_PASSWORD: string; // The password to the Redis DB

    CASSANDRA_USER: string; // The Cassandra User
    CASSANDRA_PASSWORD: string; // The password of the cassandra user
    CASSANDRA_CONTACT_POINTS: string[]; // The URLs to the cassandra nodes
    CASSANDRA_DATACENTER: string; // The datacenter

}

(async () => {

    // Main App
    dotenv.config(); // parsing env
    const env: Environment = {
        SMILIN_FILE_HOSTING_PORT: process.env.SMILIN_FILE_HOSTING_PORT != undefined ? parseInt(process.env.SMILIN_FILE_HOSTING_PORT) : 2356, // Default = Port 2356
        REDIS_URL: process.env.REDIS_URL ?? "redis://127.0.0.1", // Default => Redis in localhost
        REDIS_PASSWORD: process.env.REDIS_PASSWORD ?? "redis", // Default => Redis
        CASSANDRA_USER: process.env.CASSANDRA_USER ?? "cassandra", // Default => cassandra
        CASSANDRA_PASSWORD: process.env.CASSANDRA_PASSWORD ?? "cassandra", // Default => cassandra
        CASSANDRA_CONTACT_POINTS: process.env.CASSANDRA_CONTACT_POINTS != undefined ? process.env.CASSANDRA_CONTACT_POINTS.split("'").filter(x => x != ', ' && x != '[' && x != ']') : [], // Default => empty array
        CASSANDRA_DATACENTER: process.env.CASSANDRA_DATACENTER ?? "datacenter1", // Default => datacenter1
    };
    const app = express();
    const port = process.env.SMILIN_FILE_HOSTING_PORT;

    // Middleware
    app.use(cors());
    app.use(busboy());

    // Routes
    app.use('/rest/v1/user', UserRoutes);
    app.use('/rest/v1/files', FilesRoutes);

    // Databases
    await Redis.setup(env.REDIS_URL, env.REDIS_PASSWORD);
    await Cassandra.setup(env.CASSANDRA_USER, env.CASSANDRA_PASSWORD, env.CASSANDRA_CONTACT_POINTS, env.CASSANDRA_DATACENTER)

    // Listen
    app.listen(port, () => {
        console.log(`Smilin File Hosting Server running on Port ${port}`);
    });

})()
