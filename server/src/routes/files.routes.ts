import {Router} from "express";
import {Authorization} from "../middleware/authorization";
import {FilesController} from "../controller/files.controller";
import {FileID} from "../middleware/file-id";

const router = Router();

router.get('/describe', Authorization, FileID.QueryParams, FilesController.describeFileHandler);
router.post('/upload', Authorization, FilesController.addFileHandler);
router.put('/update', Authorization, FileID.QueryParams, FilesController.updateFileHandler);
router.delete('/delete', Authorization, FileID.QueryParams, FilesController.deleteFileHandler);

export default router;
