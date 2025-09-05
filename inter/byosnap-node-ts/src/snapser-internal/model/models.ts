import localVarRequest from 'request';

export * from './apiHttpBody';
export * from './authAnonLoginRequest';
export * from './authAnonLoginResponse';
export * from './authAppleLoginRequest';
export * from './authAppleLoginResponse';
export * from './authAssociateLoginsRequest';
export * from './authDiscordLoginRequest';
export * from './authDiscordLoginResponse';
export * from './authEmailLoginRequest';
export * from './authEmailLoginResponse';
export * from './authEmailPasswordLoginRequest';
export * from './authEmailPasswordLoginResponse';
export * from './authEpicLoginRequest';
export * from './authEpicLoginResponse';
export * from './authFacebookLoginRequest';
export * from './authFacebookLoginResponse';
export * from './authGetUserIdsByLoginIdsResponse';
export * from './authGetUsernameAvailabilityResponse';
export * from './authGoogleLoginRequest';
export * from './authGoogleLoginResponse';
export * from './authLoginId';
export * from './authLoginMetadata';
export * from './authLoginTypeType';
export * from './authOtpRequest';
export * from './authRecoverEmailAccountRequest';
export * from './authRefreshRequest';
export * from './authRefreshResponse';
export * from './authSteamLoginRequest';
export * from './authSteamLoginResponse';
export * from './authSteamOpenIdLoginRequest';
export * from './authSteamSessionTicketLoginRequest';
export * from './authSuspendUserResponse';
export * from './authUpdateEmailPasswordRequest';
export * from './authUpdateUsernamePasswordRequest';
export * from './authUser';
export * from './authUsernamePasswordLoginRequest';
export * from './authUsernamePasswordLoginResponse';
export * from './authValidateRequest';
export * from './authValidateResponse';
export * from './authVerifyEmailRequest';
export * from './authVerifyEmailResponse';
export * from './authXLoginRequest';
export * from './authXLoginResponse';
export * from './authXboxLoginRequest';
export * from './authXboxLoginResponse';
export * from './disassociateLoginRequest';
export * from './patchProfileRequest';
export * from './profilesBatchGetProfilesResponse';
export * from './profilesBatchGetProfilesSingleResponse';
export * from './profilesGetProfileRequest';
export * from './profilesGetProfileResponse';
export * from './profilesPatchProfileResponse';
export * from './profilesSearchField';
export * from './profilesSearchProfilesRequest';
export * from './profilesSearchProfilesResponse';
export * from './protobufAny';
export * from './protobufNullValue';
export * from './searchFieldOperator';
export * from './suspendUserRequest';
export * from './upsertProfileRequest';

import * as fs from 'fs';

export interface RequestDetailedFile {
    value: Buffer;
    options?: {
        filename?: string;
        contentType?: string;
    }
}

export type RequestFile = string | Buffer | fs.ReadStream | RequestDetailedFile;


import { ApiHttpBody } from './apiHttpBody';
import { AuthAnonLoginRequest } from './authAnonLoginRequest';
import { AuthAnonLoginResponse } from './authAnonLoginResponse';
import { AuthAppleLoginRequest } from './authAppleLoginRequest';
import { AuthAppleLoginResponse } from './authAppleLoginResponse';
import { AuthAssociateLoginsRequest } from './authAssociateLoginsRequest';
import { AuthDiscordLoginRequest } from './authDiscordLoginRequest';
import { AuthDiscordLoginResponse } from './authDiscordLoginResponse';
import { AuthEmailLoginRequest } from './authEmailLoginRequest';
import { AuthEmailLoginResponse } from './authEmailLoginResponse';
import { AuthEmailPasswordLoginRequest } from './authEmailPasswordLoginRequest';
import { AuthEmailPasswordLoginResponse } from './authEmailPasswordLoginResponse';
import { AuthEpicLoginRequest } from './authEpicLoginRequest';
import { AuthEpicLoginResponse } from './authEpicLoginResponse';
import { AuthFacebookLoginRequest } from './authFacebookLoginRequest';
import { AuthFacebookLoginResponse } from './authFacebookLoginResponse';
import { AuthGetUserIdsByLoginIdsResponse } from './authGetUserIdsByLoginIdsResponse';
import { AuthGetUsernameAvailabilityResponse } from './authGetUsernameAvailabilityResponse';
import { AuthGoogleLoginRequest } from './authGoogleLoginRequest';
import { AuthGoogleLoginResponse } from './authGoogleLoginResponse';
import { AuthLoginId } from './authLoginId';
import { AuthLoginMetadata } from './authLoginMetadata';
import { AuthLoginTypeType } from './authLoginTypeType';
import { AuthOtpRequest } from './authOtpRequest';
import { AuthRecoverEmailAccountRequest } from './authRecoverEmailAccountRequest';
import { AuthRefreshRequest } from './authRefreshRequest';
import { AuthRefreshResponse } from './authRefreshResponse';
import { AuthSteamLoginRequest } from './authSteamLoginRequest';
import { AuthSteamLoginResponse } from './authSteamLoginResponse';
import { AuthSteamOpenIdLoginRequest } from './authSteamOpenIdLoginRequest';
import { AuthSteamSessionTicketLoginRequest } from './authSteamSessionTicketLoginRequest';
import { AuthSuspendUserResponse } from './authSuspendUserResponse';
import { AuthUpdateEmailPasswordRequest } from './authUpdateEmailPasswordRequest';
import { AuthUpdateUsernamePasswordRequest } from './authUpdateUsernamePasswordRequest';
import { AuthUser } from './authUser';
import { AuthUsernamePasswordLoginRequest } from './authUsernamePasswordLoginRequest';
import { AuthUsernamePasswordLoginResponse } from './authUsernamePasswordLoginResponse';
import { AuthValidateRequest } from './authValidateRequest';
import { AuthValidateResponse } from './authValidateResponse';
import { AuthVerifyEmailRequest } from './authVerifyEmailRequest';
import { AuthVerifyEmailResponse } from './authVerifyEmailResponse';
import { AuthXLoginRequest } from './authXLoginRequest';
import { AuthXLoginResponse } from './authXLoginResponse';
import { AuthXboxLoginRequest } from './authXboxLoginRequest';
import { AuthXboxLoginResponse } from './authXboxLoginResponse';
import { DisassociateLoginRequest } from './disassociateLoginRequest';
import { PatchProfileRequest } from './patchProfileRequest';
import { ProfilesBatchGetProfilesResponse } from './profilesBatchGetProfilesResponse';
import { ProfilesBatchGetProfilesSingleResponse } from './profilesBatchGetProfilesSingleResponse';
import { ProfilesGetProfileRequest } from './profilesGetProfileRequest';
import { ProfilesGetProfileResponse } from './profilesGetProfileResponse';
import { ProfilesPatchProfileResponse } from './profilesPatchProfileResponse';
import { ProfilesSearchField } from './profilesSearchField';
import { ProfilesSearchProfilesRequest } from './profilesSearchProfilesRequest';
import { ProfilesSearchProfilesResponse } from './profilesSearchProfilesResponse';
import { ProtobufAny } from './protobufAny';
import { ProtobufNullValue } from './protobufNullValue';
import { SearchFieldOperator } from './searchFieldOperator';
import { SuspendUserRequest } from './suspendUserRequest';
import { UpsertProfileRequest } from './upsertProfileRequest';

/* tslint:disable:no-unused-variable */
let primitives = [
                    "string",
                    "boolean",
                    "double",
                    "integer",
                    "long",
                    "float",
                    "number",
                    "any"
                 ];

let enumsMap: {[index: string]: any} = {
        "AuthLoginTypeType": AuthLoginTypeType,
        "ProtobufNullValue": ProtobufNullValue,
        "SearchFieldOperator": SearchFieldOperator,
}

let typeMap: {[index: string]: any} = {
    "ApiHttpBody": ApiHttpBody,
    "AuthAnonLoginRequest": AuthAnonLoginRequest,
    "AuthAnonLoginResponse": AuthAnonLoginResponse,
    "AuthAppleLoginRequest": AuthAppleLoginRequest,
    "AuthAppleLoginResponse": AuthAppleLoginResponse,
    "AuthAssociateLoginsRequest": AuthAssociateLoginsRequest,
    "AuthDiscordLoginRequest": AuthDiscordLoginRequest,
    "AuthDiscordLoginResponse": AuthDiscordLoginResponse,
    "AuthEmailLoginRequest": AuthEmailLoginRequest,
    "AuthEmailLoginResponse": AuthEmailLoginResponse,
    "AuthEmailPasswordLoginRequest": AuthEmailPasswordLoginRequest,
    "AuthEmailPasswordLoginResponse": AuthEmailPasswordLoginResponse,
    "AuthEpicLoginRequest": AuthEpicLoginRequest,
    "AuthEpicLoginResponse": AuthEpicLoginResponse,
    "AuthFacebookLoginRequest": AuthFacebookLoginRequest,
    "AuthFacebookLoginResponse": AuthFacebookLoginResponse,
    "AuthGetUserIdsByLoginIdsResponse": AuthGetUserIdsByLoginIdsResponse,
    "AuthGetUsernameAvailabilityResponse": AuthGetUsernameAvailabilityResponse,
    "AuthGoogleLoginRequest": AuthGoogleLoginRequest,
    "AuthGoogleLoginResponse": AuthGoogleLoginResponse,
    "AuthLoginId": AuthLoginId,
    "AuthLoginMetadata": AuthLoginMetadata,
    "AuthOtpRequest": AuthOtpRequest,
    "AuthRecoverEmailAccountRequest": AuthRecoverEmailAccountRequest,
    "AuthRefreshRequest": AuthRefreshRequest,
    "AuthRefreshResponse": AuthRefreshResponse,
    "AuthSteamLoginRequest": AuthSteamLoginRequest,
    "AuthSteamLoginResponse": AuthSteamLoginResponse,
    "AuthSteamOpenIdLoginRequest": AuthSteamOpenIdLoginRequest,
    "AuthSteamSessionTicketLoginRequest": AuthSteamSessionTicketLoginRequest,
    "AuthSuspendUserResponse": AuthSuspendUserResponse,
    "AuthUpdateEmailPasswordRequest": AuthUpdateEmailPasswordRequest,
    "AuthUpdateUsernamePasswordRequest": AuthUpdateUsernamePasswordRequest,
    "AuthUser": AuthUser,
    "AuthUsernamePasswordLoginRequest": AuthUsernamePasswordLoginRequest,
    "AuthUsernamePasswordLoginResponse": AuthUsernamePasswordLoginResponse,
    "AuthValidateRequest": AuthValidateRequest,
    "AuthValidateResponse": AuthValidateResponse,
    "AuthVerifyEmailRequest": AuthVerifyEmailRequest,
    "AuthVerifyEmailResponse": AuthVerifyEmailResponse,
    "AuthXLoginRequest": AuthXLoginRequest,
    "AuthXLoginResponse": AuthXLoginResponse,
    "AuthXboxLoginRequest": AuthXboxLoginRequest,
    "AuthXboxLoginResponse": AuthXboxLoginResponse,
    "DisassociateLoginRequest": DisassociateLoginRequest,
    "PatchProfileRequest": PatchProfileRequest,
    "ProfilesBatchGetProfilesResponse": ProfilesBatchGetProfilesResponse,
    "ProfilesBatchGetProfilesSingleResponse": ProfilesBatchGetProfilesSingleResponse,
    "ProfilesGetProfileRequest": ProfilesGetProfileRequest,
    "ProfilesGetProfileResponse": ProfilesGetProfileResponse,
    "ProfilesPatchProfileResponse": ProfilesPatchProfileResponse,
    "ProfilesSearchField": ProfilesSearchField,
    "ProfilesSearchProfilesRequest": ProfilesSearchProfilesRequest,
    "ProfilesSearchProfilesResponse": ProfilesSearchProfilesResponse,
    "ProtobufAny": ProtobufAny,
    "SuspendUserRequest": SuspendUserRequest,
    "UpsertProfileRequest": UpsertProfileRequest,
}

export class ObjectSerializer {
    public static findCorrectType(data: any, expectedType: string) {
        if (data == undefined) {
            return expectedType;
        } else if (primitives.indexOf(expectedType.toLowerCase()) !== -1) {
            return expectedType;
        } else if (expectedType === "Date") {
            return expectedType;
        } else {
            if (enumsMap[expectedType]) {
                return expectedType;
            }

            if (!typeMap[expectedType]) {
                return expectedType; // w/e we don't know the type
            }

            // Check the discriminator
            let discriminatorProperty = typeMap[expectedType].discriminator;
            if (discriminatorProperty == null) {
                return expectedType; // the type does not have a discriminator. use it.
            } else {
                if (data[discriminatorProperty]) {
                    var discriminatorType = data[discriminatorProperty];
                    if(typeMap[discriminatorType]){
                        return discriminatorType; // use the type given in the discriminator
                    } else {
                        return expectedType; // discriminator did not map to a type
                    }
                } else {
                    return expectedType; // discriminator was not present (or an empty string)
                }
            }
        }
    }

    public static serialize(data: any, type: string) {
        if (data == undefined) {
            return data;
        } else if (primitives.indexOf(type.toLowerCase()) !== -1) {
            return data;
        } else if (type.lastIndexOf("Array<", 0) === 0) { // string.startsWith pre es6
            let subType: string = type.replace("Array<", ""); // Array<Type> => Type>
            subType = subType.substring(0, subType.length - 1); // Type> => Type
            let transformedData: any[] = [];
            for (let index = 0; index < data.length; index++) {
                let datum = data[index];
                transformedData.push(ObjectSerializer.serialize(datum, subType));
            }
            return transformedData;
        } else if (type === "Date") {
            return data.toISOString();
        } else {
            if (enumsMap[type]) {
                return data;
            }
            if (!typeMap[type]) { // in case we dont know the type
                return data;
            }

            // Get the actual type of this object
            type = this.findCorrectType(data, type);

            // get the map for the correct type.
            let attributeTypes = typeMap[type].getAttributeTypeMap();
            let instance: {[index: string]: any} = {};
            for (let index = 0; index < attributeTypes.length; index++) {
                let attributeType = attributeTypes[index];
                instance[attributeType.baseName] = ObjectSerializer.serialize(data[attributeType.name], attributeType.type);
            }
            return instance;
        }
    }

    public static deserialize(data: any, type: string) {
        // polymorphism may change the actual type.
        type = ObjectSerializer.findCorrectType(data, type);
        if (data == undefined) {
            return data;
        } else if (primitives.indexOf(type.toLowerCase()) !== -1) {
            return data;
        } else if (type.lastIndexOf("Array<", 0) === 0) { // string.startsWith pre es6
            let subType: string = type.replace("Array<", ""); // Array<Type> => Type>
            subType = subType.substring(0, subType.length - 1); // Type> => Type
            let transformedData: any[] = [];
            for (let index = 0; index < data.length; index++) {
                let datum = data[index];
                transformedData.push(ObjectSerializer.deserialize(datum, subType));
            }
            return transformedData;
        } else if (type === "Date") {
            return new Date(data);
        } else {
            if (enumsMap[type]) {// is Enum
                return data;
            }

            if (!typeMap[type]) { // dont know the type
                return data;
            }
            let instance = new typeMap[type]();
            let attributeTypes = typeMap[type].getAttributeTypeMap();
            for (let index = 0; index < attributeTypes.length; index++) {
                let attributeType = attributeTypes[index];
                instance[attributeType.name] = ObjectSerializer.deserialize(data[attributeType.baseName], attributeType.type);
            }
            return instance;
        }
    }
}

export interface Authentication {
    /**
    * Apply authentication settings to header and query params.
    */
    applyToRequest(requestOptions: localVarRequest.Options): Promise<void> | void;
}

export class HttpBasicAuth implements Authentication {
    public username: string = '';
    public password: string = '';

    applyToRequest(requestOptions: localVarRequest.Options): void {
        requestOptions.auth = {
            username: this.username, password: this.password
        }
    }
}

export class HttpBearerAuth implements Authentication {
    public accessToken: string | (() => string) = '';

    applyToRequest(requestOptions: localVarRequest.Options): void {
        if (requestOptions && requestOptions.headers) {
            const accessToken = typeof this.accessToken === 'function'
                            ? this.accessToken()
                            : this.accessToken;
            requestOptions.headers["Authorization"] = "Bearer " + accessToken;
        }
    }
}

export class ApiKeyAuth implements Authentication {
    public apiKey: string = '';

    constructor(private location: string, private paramName: string) {
    }

    applyToRequest(requestOptions: localVarRequest.Options): void {
        if (this.location == "query") {
            (<any>requestOptions.qs)[this.paramName] = this.apiKey;
        } else if (this.location == "header" && requestOptions && requestOptions.headers) {
            requestOptions.headers[this.paramName] = this.apiKey;
        } else if (this.location == 'cookie' && requestOptions && requestOptions.headers) {
            if (requestOptions.headers['Cookie']) {
                requestOptions.headers['Cookie'] += '; ' + this.paramName + '=' + encodeURIComponent(this.apiKey);
            }
            else {
                requestOptions.headers['Cookie'] = this.paramName + '=' + encodeURIComponent(this.apiKey);
            }
        }
    }
}

export class OAuth implements Authentication {
    public accessToken: string = '';

    applyToRequest(requestOptions: localVarRequest.Options): void {
        if (requestOptions && requestOptions.headers) {
            requestOptions.headers["Authorization"] = "Bearer " + this.accessToken;
        }
    }
}

export class VoidAuth implements Authentication {
    public username: string = '';
    public password: string = '';

    applyToRequest(_: localVarRequest.Options): void {
        // Do nothing
    }
}

export type Interceptor = (requestOptions: localVarRequest.Options) => (Promise<void> | void);
