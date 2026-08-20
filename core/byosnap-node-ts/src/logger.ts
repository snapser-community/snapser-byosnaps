import { AsyncLocalStorage } from 'node:async_hooks';
import type { NextFunction, Request, Response } from 'express';

// Snapser parses `level` to color the line in the Logs tool and correlates all
// log lines of one request by the `request-id` field (from the X-Request-Id header).
const requestIdStore = new AsyncLocalStorage<string>();

export const REQUEST_ID_HEADER_KEY = 'X-Request-Id';

type Level = 'debug' | 'info' | 'warn' | 'error';

function write(level: Level, message: string, fields?: Record<string, unknown>): void {
    const entry: Record<string, unknown> = {
        level,
        message,
        timestamp: new Date().toISOString(),
        ...fields,
    };
    const requestId = requestIdStore.getStore();
    if (requestId) {
        entry['request-id'] = requestId;
    }
    console.log(JSON.stringify(entry));
}

export const logger = {
    debug: (message: string, fields?: Record<string, unknown>) => write('debug', message, fields),
    info: (message: string, fields?: Record<string, unknown>) => write('info', message, fields),
    warn: (message: string, fields?: Record<string, unknown>) => write('warn', message, fields),
    error: (message: string, fields?: Record<string, unknown>) => write('error', message, fields),
};

// Returns the current request's id, for forwarding on outbound snap-to-snap calls.
export function getRequestId(): string {
    return requestIdStore.getStore() ?? '';
}

// X-Request-Id is client-supplied: cap the length and allow only safe chars.
function sanitizeRequestId(value: string): string {
    const truncated = value.slice(0, 128);
    return /^[A-Za-z0-9._-]*$/.test(truncated) ? truncated : '';
}

// Express middleware: binds X-Request-Id for every log line in this request.
export function requestIdMiddleware(req: Request, _res: Response, next: NextFunction): void {
    requestIdStore.run(sanitizeRequestId(req.header(REQUEST_ID_HEADER_KEY) ?? ''), () => next());
}
