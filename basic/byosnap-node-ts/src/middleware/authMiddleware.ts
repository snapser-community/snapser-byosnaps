import { Request, Response, NextFunction } from 'express';
import { ErrorResponse } from '../types/responses';

// Define constants for auth types and headers as in the previous example
const AUTH_TYPE_HEADER_KEY = 'Auth-Type';
const USER_ID_HEADER_KEY = 'User-Id';
const GATEWAY_HEADER_KEY = 'Gateway';
const GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE = 'internal';
const AUTH_TYPE_HEADER_VALUE_USER_AUTH = 'user';
const AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH = 'api-key';

export const authMiddleware = (allowedAuthTypes: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    const gatewayHeaders = req.headers[GATEWAY_HEADER_KEY.toLowerCase()];
    const authTypeHeaders = req.headers[AUTH_TYPE_HEADER_KEY.toLowerCase()];
    const userIdHeaders = req.headers[USER_ID_HEADER_KEY.toLowerCase()];
    let gatewayHeader: string = ''
    let authTypeHeader: string = ''
    let userIdHeader: string = ''
    if(gatewayHeaders) {
        gatewayHeader = Array.isArray(gatewayHeaders) ? gatewayHeaders[0].toLowerCase() : gatewayHeaders.toLowerCase();
    }
    if(authTypeHeaders) {
        authTypeHeader = Array.isArray(authTypeHeaders) ? authTypeHeaders[0].toLowerCase() : authTypeHeaders.toLowerCase();
    }
    if(userIdHeaders) {
        userIdHeader = Array.isArray(userIdHeaders) ? userIdHeaders[0].toLowerCase() : userIdHeaders.toLowerCase();
    }
    const targetUser = req.params['userId'] ?? '';
    const isInternalCall = gatewayHeader === GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE.toLowerCase();
    const isApiKeyAuth = authTypeHeader === AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH.toLowerCase();
    const isTargetUser = userIdHeader === targetUser.toLowerCase();

    let isAuthorized = false;
    for(let i = 0; i < allowedAuthTypes.length; i++) {
        if(authTypeHeader === GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE.toLowerCase()) {
            if(!isInternalCall) {
                continue;
            }
            isAuthorized = true;
        }
        else if(authTypeHeader === AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH.toLowerCase()) {
            if(!isInternalCall && !isApiKeyAuth) {
                continue;
            }
            isAuthorized = true;
        }
        else if(authTypeHeader === AUTH_TYPE_HEADER_VALUE_USER_AUTH.toLowerCase()) {
            if(!isInternalCall && !isApiKeyAuth && !isTargetUser) {
                continue;
            }
            isAuthorized = true;
        }
    }

    if (!isAuthorized) {
        let errorResponse: ErrorResponse = {
            error_message: 'Unauthorized'
        };
        return res.status(401).json(errorResponse);
    }
    next();
  };
};
