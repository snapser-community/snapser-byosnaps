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
    let gatewayHeaderValue: string = ''
    let authTypeHeaderValue: string = ''
    let userIdHeaderValue: string = ''
    if(gatewayHeaders) {
        gatewayHeaderValue = Array.isArray(gatewayHeaders) ? gatewayHeaders[0].toLowerCase() : gatewayHeaders.toLowerCase();
    }
    if(authTypeHeaders) {
        authTypeHeaderValue = Array.isArray(authTypeHeaders) ? authTypeHeaders[0].toLowerCase() : authTypeHeaders.toLowerCase();
    }
    if(userIdHeaders) {
        userIdHeaderValue = Array.isArray(userIdHeaders) ? userIdHeaders[0].toLowerCase() : userIdHeaders.toLowerCase();
    }
    // If the API has a URL parameter for user_id, then use that
    // Otherwise, use the User-Id header value as the default
    const targetUser = req.params['userId'] ?? userIdHeaderValue;
    const isInternalCall = gatewayHeaderValue.toLowerCase() === GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE;
    const isApiKeyAuth = authTypeHeaderValue.toLowerCase() === AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH;
    const isTargetUser = userIdHeaderValue === targetUser && userIdHeaderValue !== '';
    let isAuthorized = false;
    for(let i = 0; i < allowedAuthTypes.length; i++) {
        if(allowedAuthTypes[i] === GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE) {
            if(!isInternalCall) {
                continue;
            }
            isAuthorized = true;
        }
        else if(allowedAuthTypes[i] === AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH) {
            if(!isInternalCall && !isApiKeyAuth) {
                continue;
            }
            isAuthorized = true;
        }
        else if(allowedAuthTypes[i] === AUTH_TYPE_HEADER_VALUE_USER_AUTH) {
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
