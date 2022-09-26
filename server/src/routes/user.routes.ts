import {Router} from "express";
import {UserController} from "../controller/user.controller";
import {Authorization} from "../middleware/authorization";

const router = Router();

router.post('/register', UserController.registerHandler);
router.post('/login', Authorization, UserController.loginHandler);
router.delete('/delete', Authorization, UserController.deleteAccountHandler)

export default router;
