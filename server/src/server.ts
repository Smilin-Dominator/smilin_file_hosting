import Redis from "./util/redis";
import Cassandra from "./util/cassandra";
import express from "express";
import cors from "cors";
import busboy from "connect-busboy";
import UserRoutes from "./routes/user.routes";
import FilesRoutes from "./routes/files.routes";

(async () => {

    // Main App
    const app = express();
    const port = 2356;

    // Middleware
    app.use(cors());
    app.use(busboy());

    // Routes
    app.use('/rest/v1/user', UserRoutes);
    app.use('/rest/v1/files', FilesRoutes);

    // Databases
    await Redis.setup('redis://127.0.0.1', 'z-crBrrXvDm@!or@fA33');
    await Cassandra.setup('api', 'Nhth3td.ZY_@wHw9agws' , ['127.0.0.1']);

    // Listen
    app.listen(port, () => {
        console.log(`Smilin File Hosting Server running on Port ${port}`);
    });

})()
