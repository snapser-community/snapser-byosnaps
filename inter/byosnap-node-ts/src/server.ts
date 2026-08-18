import { app } from './app';
import { logger } from './logger';

//This is important - Unless you import your controllers, the tsoa generated routes will not be registered
import './controllers/usersController';

const PORT = process.env.PORT || 5003;
app.listen(PORT, () => {
    logger.info(`Server is running at http://localhost:${PORT}`);
});
