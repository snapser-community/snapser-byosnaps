export * from './authServiceApi';
import { AuthServiceApi } from './authServiceApi';
export * from './profilesServiceApi';
import { ProfilesServiceApi } from './profilesServiceApi';
import * as http from 'http';

export class HttpError extends Error {
    constructor (public response: http.IncomingMessage, public body: any, public statusCode?: number) {
        super('HTTP request failed');
        this.name = 'HttpError';
    }
}

export { RequestFile } from '../model/models';

export const APIS = [AuthServiceApi, ProfilesServiceApi];
