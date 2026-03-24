/* tslint:disable */
/* eslint-disable */
// WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
import type { TsoaRoute } from '@tsoa/runtime';
import {  fetchMiddlewares, ExpressTemplateService } from '@tsoa/runtime';
// WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
import { SettingsController } from './controllers/settingsController';
// WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
import { CharactersController } from './controllers/charactersController';
import type { Request as ExRequest, Response as ExResponse, RequestHandler, Router } from 'express';



// WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

const models: TsoaRoute.Models = {
    "SettingsComponent": {
        "dataType": "refObject",
        "properties": {
            "id": {"dataType":"string","required":true},
            "type": {"dataType":"string","required":true},
            "value": {"dataType":"string","required":true},
        },
        "additionalProperties": false,
    },
    // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
    "SettingsSection": {
        "dataType": "refObject",
        "properties": {
            "id": {"dataType":"string","required":true},
            "components": {"dataType":"array","array":{"dataType":"refObject","ref":"SettingsComponent"},"required":true},
        },
        "additionalProperties": false,
    },
    // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
    "SettingsSchema": {
        "dataType": "refObject",
        "properties": {
            "sections": {"dataType":"array","array":{"dataType":"refObject","ref":"SettingsSection"},"required":true},
        },
        "additionalProperties": false,
    },
    // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
    "ErrorResponse": {
        "dataType": "refAlias",
        "type": {"dataType":"nestedObjectLiteral","nestedProperties":{"error_message":{"dataType":"string","required":true}},"validators":{}},
    },
    // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
    "Record_string.any_": {
        "dataType": "refAlias",
        "type": {"dataType":"nestedObjectLiteral","nestedProperties":{},"additionalProperties":{"dataType":"any"},"validators":{}},
    },
    // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
    "CustomSettingsPayload": {
        "dataType": "refObject",
        "properties": {
            "payload": {"dataType":"any","required":true},
        },
        "additionalProperties": false,
    },
    // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
    "ExportSettingsSchema": {
        "dataType": "refObject",
        "properties": {
            "version": {"dataType":"string","required":true},
            "exported_at": {"dataType":"double","required":true},
            "data": {"dataType":"nestedObjectLiteral","nestedProperties":{},"additionalProperties":{"dataType":"nestedObjectLiteral","nestedProperties":{},"additionalProperties":{"ref":"SettingsSchema"}},"required":true},
        },
        "additionalProperties": false,
    },
    // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
    "SuccessMessageResponse": {
        "dataType": "refAlias",
        "type": {"dataType":"nestedObjectLiteral","nestedProperties":{"message":{"dataType":"string","required":true}},"validators":{}},
    },
    // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
    "CharactersResponse": {
        "dataType": "refObject",
        "properties": {
            "characters": {"dataType":"array","array":{"dataType":"string"},"required":true},
        },
        "additionalProperties": false,
    },
    // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
};
const templateService = new ExpressTemplateService(models, {"noImplicitAdditionalProperties":"throw-on-extras","bodyCoercion":true});

// WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa




export function RegisterRoutes(app: Router) {

    // ###########################################################################################################
    //  NOTE: If you do not see routes for all of your controllers in this file, then you might not have informed tsoa of where to look
    //      Please look into the "controllerPathGlobs" config option described in the readme: https://github.com/lukeautry/tsoa
    // ###########################################################################################################


    
        const argsSettingsController_getSettings: Record<string, TsoaRoute.ParameterSchema> = {
                _unauthorized: {"in":"res","name":"401","required":true,"ref":"ErrorResponse"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
                tool_id: {"in":"query","name":"tool_id","dataType":"string"},
                environment: {"in":"query","name":"environment","dataType":"string"},
        };
        app.get('/v1/byosnap-advanced/settings',
            ...(fetchMiddlewares<RequestHandler>(SettingsController)),
            ...(fetchMiddlewares<RequestHandler>(SettingsController.prototype.getSettings)),

            async function SettingsController_getSettings(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsSettingsController_getSettings, request, response });

                const controller = new SettingsController();

              await templateService.apiHandler({
                methodName: 'getSettings',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
        const argsSettingsController_updateSettings: Record<string, TsoaRoute.ParameterSchema> = {
                _badRequest: {"in":"res","name":"400","required":true,"ref":"ErrorResponse"},
                _serverError: {"in":"res","name":"500","required":true,"ref":"ErrorResponse"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
                body: {"in":"body","name":"body","required":true,"ref":"Record_string.any_"},
                tool_id: {"in":"query","name":"tool_id","dataType":"string"},
                environment: {"in":"query","name":"environment","dataType":"string"},
        };
        app.put('/v1/byosnap-advanced/settings',
            ...(fetchMiddlewares<RequestHandler>(SettingsController)),
            ...(fetchMiddlewares<RequestHandler>(SettingsController.prototype.updateSettings)),

            async function SettingsController_updateSettings(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsSettingsController_updateSettings, request, response });

                const controller = new SettingsController();

              await templateService.apiHandler({
                methodName: 'updateSettings',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
        const argsSettingsController_getSettingsCustom: Record<string, TsoaRoute.ParameterSchema> = {
                _unauthorized: {"in":"res","name":"401","required":true,"ref":"ErrorResponse"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
                tool_id: {"in":"query","name":"tool_id","dataType":"string"},
                environment: {"in":"query","name":"environment","dataType":"string"},
        };
        app.get('/v1/byosnap-advanced/settings/custom',
            ...(fetchMiddlewares<RequestHandler>(SettingsController)),
            ...(fetchMiddlewares<RequestHandler>(SettingsController.prototype.getSettingsCustom)),

            async function SettingsController_getSettingsCustom(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsSettingsController_getSettingsCustom, request, response });

                const controller = new SettingsController();

              await templateService.apiHandler({
                methodName: 'getSettingsCustom',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
        const argsSettingsController_updateSettingsCustom: Record<string, TsoaRoute.ParameterSchema> = {
                _serverError: {"in":"res","name":"500","required":true,"ref":"ErrorResponse"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
                body: {"in":"body","name":"body","required":true,"ref":"Record_string.any_"},
                tool_id: {"in":"query","name":"tool_id","dataType":"string"},
                environment: {"in":"query","name":"environment","dataType":"string"},
        };
        app.put('/v1/byosnap-advanced/settings/custom',
            ...(fetchMiddlewares<RequestHandler>(SettingsController)),
            ...(fetchMiddlewares<RequestHandler>(SettingsController.prototype.updateSettingsCustom)),

            async function SettingsController_updateSettingsCustom(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsSettingsController_updateSettingsCustom, request, response });

                const controller = new SettingsController();

              await templateService.apiHandler({
                methodName: 'updateSettingsCustom',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
        const argsSettingsController_exportSettings: Record<string, TsoaRoute.ParameterSchema> = {
                _serverError: {"in":"res","name":"500","required":true,"ref":"ErrorResponse"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
        };
        app.get('/v1/byosnap-advanced/settings/export',
            ...(fetchMiddlewares<RequestHandler>(SettingsController)),
            ...(fetchMiddlewares<RequestHandler>(SettingsController.prototype.exportSettings)),

            async function SettingsController_exportSettings(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsSettingsController_exportSettings, request, response });

                const controller = new SettingsController();

              await templateService.apiHandler({
                methodName: 'exportSettings',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
        const argsSettingsController_importSettings: Record<string, TsoaRoute.ParameterSchema> = {
                _badRequest: {"in":"res","name":"400","required":true,"ref":"ErrorResponse"},
                _serverError: {"in":"res","name":"500","required":true,"ref":"ErrorResponse"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
                body: {"in":"body","name":"body","required":true,"ref":"ExportSettingsSchema"},
        };
        app.post('/v1/byosnap-advanced/settings/import',
            ...(fetchMiddlewares<RequestHandler>(SettingsController)),
            ...(fetchMiddlewares<RequestHandler>(SettingsController.prototype.importSettings)),

            async function SettingsController_importSettings(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsSettingsController_importSettings, request, response });

                const controller = new SettingsController();

              await templateService.apiHandler({
                methodName: 'importSettings',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
        const argsSettingsController_validateImportSettings: Record<string, TsoaRoute.ParameterSchema> = {
                _serverError: {"in":"res","name":"500","required":true,"ref":"ErrorResponse"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
                body: {"in":"body","name":"body","required":true,"ref":"ExportSettingsSchema"},
        };
        app.post('/v1/byosnap-advanced/settings/validate-import',
            ...(fetchMiddlewares<RequestHandler>(SettingsController)),
            ...(fetchMiddlewares<RequestHandler>(SettingsController.prototype.validateImportSettings)),

            async function SettingsController_validateImportSettings(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsSettingsController_validateImportSettings, request, response });

                const controller = new SettingsController();

              await templateService.apiHandler({
                methodName: 'validateImportSettings',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
        const argsSettingsController_getUserDataCustom: Record<string, TsoaRoute.ParameterSchema> = {
                _unauthorized: {"in":"res","name":"401","required":true,"ref":"ErrorResponse"},
                userId: {"in":"path","name":"userId","required":true,"dataType":"string"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
        };
        app.get('/v1/byosnap-advanced/settings/users/:userId/custom',
            ...(fetchMiddlewares<RequestHandler>(SettingsController)),
            ...(fetchMiddlewares<RequestHandler>(SettingsController.prototype.getUserDataCustom)),

            async function SettingsController_getUserDataCustom(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsSettingsController_getUserDataCustom, request, response });

                const controller = new SettingsController();

              await templateService.apiHandler({
                methodName: 'getUserDataCustom',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
        const argsSettingsController_updateUserDataCustom: Record<string, TsoaRoute.ParameterSchema> = {
                _serverError: {"in":"res","name":"500","required":true,"ref":"ErrorResponse"},
                userId: {"in":"path","name":"userId","required":true,"dataType":"string"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
                body: {"in":"body","name":"body","required":true,"ref":"Record_string.any_"},
        };
        app.post('/v1/byosnap-advanced/settings/users/:userId/custom',
            ...(fetchMiddlewares<RequestHandler>(SettingsController)),
            ...(fetchMiddlewares<RequestHandler>(SettingsController.prototype.updateUserDataCustom)),

            async function SettingsController_updateUserDataCustom(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsSettingsController_updateUserDataCustom, request, response });

                const controller = new SettingsController();

              await templateService.apiHandler({
                methodName: 'updateUserDataCustom',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
        const argsSettingsController_getUserData: Record<string, TsoaRoute.ParameterSchema> = {
                _badRequest: {"in":"res","name":"400","required":true,"ref":"ErrorResponse"},
                _unauthorized: {"in":"res","name":"401","required":true,"ref":"ErrorResponse"},
                userId: {"in":"path","name":"userId","required":true,"dataType":"string"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
        };
        app.get('/v1/byosnap-advanced/settings/users/:userId/data',
            ...(fetchMiddlewares<RequestHandler>(SettingsController)),
            ...(fetchMiddlewares<RequestHandler>(SettingsController.prototype.getUserData)),

            async function SettingsController_getUserData(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsSettingsController_getUserData, request, response });

                const controller = new SettingsController();

              await templateService.apiHandler({
                methodName: 'getUserData',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
        const argsSettingsController_updateUserData: Record<string, TsoaRoute.ParameterSchema> = {
                _unauthorized: {"in":"res","name":"401","required":true,"ref":"ErrorResponse"},
                userId: {"in":"path","name":"userId","required":true,"dataType":"string"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
        };
        app.put('/v1/byosnap-advanced/settings/users/:userId/data',
            ...(fetchMiddlewares<RequestHandler>(SettingsController)),
            ...(fetchMiddlewares<RequestHandler>(SettingsController.prototype.updateUserData)),

            async function SettingsController_updateUserData(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsSettingsController_updateUserData, request, response });

                const controller = new SettingsController();

              await templateService.apiHandler({
                methodName: 'updateUserData',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
        const argsSettingsController_deleteUserData: Record<string, TsoaRoute.ParameterSchema> = {
                _badRequest: {"in":"res","name":"400","required":true,"ref":"ErrorResponse"},
                _unauthorized: {"in":"res","name":"401","required":true,"ref":"ErrorResponse"},
                userId: {"in":"path","name":"userId","required":true,"dataType":"string"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
        };
        app.delete('/v1/byosnap-advanced/settings/users/:userId/data',
            ...(fetchMiddlewares<RequestHandler>(SettingsController)),
            ...(fetchMiddlewares<RequestHandler>(SettingsController.prototype.deleteUserData)),

            async function SettingsController_deleteUserData(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsSettingsController_deleteUserData, request, response });

                const controller = new SettingsController();

              await templateService.apiHandler({
                methodName: 'deleteUserData',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
        const argsCharactersController_getActiveCharacters: Record<string, TsoaRoute.ParameterSchema> = {
                _unauthorized: {"in":"res","name":"401","required":true,"ref":"ErrorResponse"},
                userId: {"in":"path","name":"userId","required":true,"dataType":"string"},
                req: {"in":"request","name":"req","required":true,"dataType":"object"},
        };
        app.get('/v1/byosnap-advanced/users/:userId/characters/active',
            ...(fetchMiddlewares<RequestHandler>(CharactersController)),
            ...(fetchMiddlewares<RequestHandler>(CharactersController.prototype.getActiveCharacters)),

            async function CharactersController_getActiveCharacters(request: ExRequest, response: ExResponse, next: any) {

            // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

            let validatedArgs: any[] = [];
            try {
                validatedArgs = templateService.getValidatedArgs({ args: argsCharactersController_getActiveCharacters, request, response });

                const controller = new CharactersController();

              await templateService.apiHandler({
                methodName: 'getActiveCharacters',
                controller,
                response,
                next,
                validatedArgs,
                successStatus: undefined,
              });
            } catch (err) {
                return next(err);
            }
        });
        // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa

    // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa


    // WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
}

// WARNING: This file was auto-generated with tsoa. Please do not modify it. Re-run tsoa to re-generate this file: https://github.com/lukeautry/tsoa
