import { app } from './app';

//This is important - Unless you import your controllers, the tsoa generated routes will not be registered
import './controllers/settingsController';
import './controllers/charactersController';

const PORT = process.env.PORT || 5003;
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
