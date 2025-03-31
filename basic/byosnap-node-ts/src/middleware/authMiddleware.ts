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
    const gatewayHeader = req.headers[GATEWAY_HEADER_KEY];
    const authTypeHeader = req.headers[AUTH_TYPE_HEADER_KEY];
    const userIdHeader = req.headers[USER_ID_HEADER_KEY];
    const targetUser = req.params['userId'];

    const isInternalCall = gatewayHeader === GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE;
    const isApiKeyAuth = authTypeHeader === AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH;
    const isTargetUser = userIdHeader === targetUser;

    let isAuthorized = false;
    for(let i = 0; i < allowedAuthTypes.length; i++) {
        const authType = allowedAuthTypes[i];
        if(authType === GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE) {
            if(!isInternalCall) {
                continue;
            }
            isAuthorized = true;
        }
        else if(authType === AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH) {
            if(!isInternalCall && !isApiKeyAuth) {
                continue;
            }
            isAuthorized = true;
        }
        else if(authType === AUTH_TYPE_HEADER_VALUE_USER_AUTH) {
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
