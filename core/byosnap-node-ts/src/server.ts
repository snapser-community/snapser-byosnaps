import { app } from './app';
import { registerEventTypes } from './eventbus';

//This is important - Unless you import your controllers, the tsoa generated routes will not be registered
import './controllers/settingsController';
import './controllers/exampleController';

const PORT = process.env.PORT || 5003;
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});

// Register this Snap's custom Eventbus event types once, on startup.
// Best-effort: this never throws, so it can't block boot or /healthz.
registerEventTypes();
