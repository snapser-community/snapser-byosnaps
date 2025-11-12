export * from './authServiceApi';
import { AuthServiceApi } from './authServiceApi';
export * from './defaultApi';
import { DefaultApi } from './defaultApi';
export * from './storageServiceApi';
import { StorageServiceApi } from './storageServiceApi';
import * as http from 'http';

export class HttpError extends Error {
    constructor (public response: http.IncomingMessage, public body: any, public statusCode?: number) {
        super('HTTP request failed');
        this.name = 'HttpError';
    }
}

export { RequestFile } from '../model/models';

export const APIS = [AuthServiceApi, DefaultApi, StorageServiceApi];
