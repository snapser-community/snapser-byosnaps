import localVarRequest from 'request';

export * from './apiHttpBody';
export * from './appendArrSubDocumentRequest';
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
export * from './errorResponseSchema';
export * from './errorResponseSchemaId';
export * from './incrementCounterRequest';
export * from './insertBlobRequest';
export * from './insertJsonBlobRequest';
export * from './mCPRequestSchema';
export * from './mCPRequestSchemaId';
export * from './prependArrSubDocumentRequest';
export * from './protobufAny';
export * from './protobufNullValue';
export * from './replaceBlobRequest';
export * from './replaceJsonBlobRequest';
export * from './storageAppendArrSubDocumentRequest';
export * from './storageAppendArrSubDocumentResponse';
export * from './storageAppendBlobAndOwner';
export * from './storageBatchAppendArrSubDocumentSingleResponse';
export * from './storageBatchAppendArrSubDocumentsRequest';
export * from './storageBatchAppendArrSubDocumentsResponse';
export * from './storageBatchDeleteJsonBlobsRequest';
export * from './storageBatchDeleteJsonBlobsResponse';
export * from './storageBatchDeleteJsonBlobsSingleResponse';
export * from './storageBatchDeleteSubDocumentSingleResponse';
export * from './storageBatchDeleteSubDocumentsRequest';
export * from './storageBatchDeleteSubDocumentsResponse';
export * from './storageBatchGetAppendBlobsResponse';
export * from './storageBatchGetAppendBlobsSingleResponse';
export * from './storageBatchGetBlobsResponse';
export * from './storageBatchGetBlobsSingleResponse';
export * from './storageBatchGetCountersResponse';
export * from './storageBatchGetCountersSingleResponse';
export * from './storageBatchGetJsonBlobsRequest';
export * from './storageBatchGetJsonBlobsResponse';
export * from './storageBatchGetJsonBlobsSingleResponse';
export * from './storageBatchGetSubDocumentsRequest';
export * from './storageBatchGetSubDocumentsResponse';
export * from './storageBatchGetSubDocumentsSingleResponse';
export * from './storageBatchIncrementCounterRequest';
export * from './storageBatchIncrementCounterResponse';
export * from './storageBatchInsertBlobRequest';
export * from './storageBatchInsertBlobResponse';
export * from './storageBatchInsertJsonBlobSingleResponse';
export * from './storageBatchInsertJsonBlobsRequest';
export * from './storageBatchInsertJsonBlobsResponse';
export * from './storageBatchPrependArrSubDocumentSingleResponse';
export * from './storageBatchPrependArrSubDocumentsRequest';
export * from './storageBatchPrependArrSubDocumentsResponse';
export * from './storageBatchReplaceBlobRequest';
export * from './storageBatchReplaceBlobResponse';
export * from './storageBatchReplaceJsonBlobSingleResponse';
export * from './storageBatchReplaceJsonBlobsRequest';
export * from './storageBatchReplaceJsonBlobsResponse';
export * from './storageBatchSingleBlobResponse';
export * from './storageBatchSingleIncrementCounterResponse';
export * from './storageBatchSingleReplaceBlobResponse';
export * from './storageBatchSingleUpdateAppendBlobResponse';
export * from './storageBatchUpdateAppendBlobRequest';
export * from './storageBatchUpdateAppendBlobResponse';
export * from './storageBatchUpsertSubDocumentSingleResponse';
export * from './storageBatchUpsertSubDocumentsRequest';
export * from './storageBatchUpsertSubDocumentsResponse';
export * from './storageBlobAndOwner';
export * from './storageCounterAndOwner';
export * from './storageDeleteAppendBlobResponse';
export * from './storageDeleteBlobResponse';
export * from './storageDeleteJsonBlobRequest';
export * from './storageDeleteJsonBlobResponse';
export * from './storageDeleteSubDocumentRequest';
export * from './storageDeleteSubDocumentResponse';
export * from './storageGetAppendBlobRequest';
export * from './storageGetAppendBlobResponse';
export * from './storageGetBlobRequest';
export * from './storageGetBlobResponse';
export * from './storageGetCasResponse';
export * from './storageGetCounterRequest';
export * from './storageGetCounterResponse';
export * from './storageGetJsonBlobRequest';
export * from './storageGetJsonBlobResponse';
export * from './storageGetSubDocumentRequest';
export * from './storageGetSubDocumentResponse';
export * from './storageIncrementCounterRequest';
export * from './storageIncrementCounterResponse';
export * from './storageInsertBlobRequest';
export * from './storageInsertBlobResponse';
export * from './storageInsertJsonBlobRequest';
export * from './storageInsertJsonBlobResponse';
export * from './storageJsonFragment';
export * from './storagePrependArrSubDocumentRequest';
export * from './storagePrependArrSubDocumentResponse';
export * from './storageReplaceBlobRequest';
export * from './storageReplaceBlobResponse';
export * from './storageReplaceJsonBlobRequest';
export * from './storageReplaceJsonBlobResponse';
export * from './storageResetCounterResponse';
export * from './storageUpdateAppendBlobRequest';
export * from './storageUpdateAppendBlobResponse';
export * from './storageUpsertSubDocumentRequest';
export * from './storageUpsertSubDocumentResponse';
export * from './storageUserAppendBlobResponse';
export * from './storageUserBlobResponse';
export * from './storageUserCounterResponse';
export * from './successResponseSchema';
export * from './successResponseSchemaId';
export * from './suspendUserRequest';
export * from './updateAppendBlobRequest';
export * from './upsertSubDocumentRequest';

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
import { AppendArrSubDocumentRequest } from './appendArrSubDocumentRequest';
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
import { ErrorResponseSchema } from './errorResponseSchema';
import { ErrorResponseSchemaId } from './errorResponseSchemaId';
import { IncrementCounterRequest } from './incrementCounterRequest';
import { InsertBlobRequest } from './insertBlobRequest';
import { InsertJsonBlobRequest } from './insertJsonBlobRequest';
import { MCPRequestSchema } from './mCPRequestSchema';
import { MCPRequestSchemaId } from './mCPRequestSchemaId';
import { PrependArrSubDocumentRequest } from './prependArrSubDocumentRequest';
import { ProtobufAny } from './protobufAny';
import { ProtobufNullValue } from './protobufNullValue';
import { ReplaceBlobRequest } from './replaceBlobRequest';
import { ReplaceJsonBlobRequest } from './replaceJsonBlobRequest';
import { StorageAppendArrSubDocumentRequest } from './storageAppendArrSubDocumentRequest';
import { StorageAppendArrSubDocumentResponse } from './storageAppendArrSubDocumentResponse';
import { StorageAppendBlobAndOwner } from './storageAppendBlobAndOwner';
import { StorageBatchAppendArrSubDocumentSingleResponse } from './storageBatchAppendArrSubDocumentSingleResponse';
import { StorageBatchAppendArrSubDocumentsRequest } from './storageBatchAppendArrSubDocumentsRequest';
import { StorageBatchAppendArrSubDocumentsResponse } from './storageBatchAppendArrSubDocumentsResponse';
import { StorageBatchDeleteJsonBlobsRequest } from './storageBatchDeleteJsonBlobsRequest';
import { StorageBatchDeleteJsonBlobsResponse } from './storageBatchDeleteJsonBlobsResponse';
import { StorageBatchDeleteJsonBlobsSingleResponse } from './storageBatchDeleteJsonBlobsSingleResponse';
import { StorageBatchDeleteSubDocumentSingleResponse } from './storageBatchDeleteSubDocumentSingleResponse';
import { StorageBatchDeleteSubDocumentsRequest } from './storageBatchDeleteSubDocumentsRequest';
import { StorageBatchDeleteSubDocumentsResponse } from './storageBatchDeleteSubDocumentsResponse';
import { StorageBatchGetAppendBlobsResponse } from './storageBatchGetAppendBlobsResponse';
import { StorageBatchGetAppendBlobsSingleResponse } from './storageBatchGetAppendBlobsSingleResponse';
import { StorageBatchGetBlobsResponse } from './storageBatchGetBlobsResponse';
import { StorageBatchGetBlobsSingleResponse } from './storageBatchGetBlobsSingleResponse';
import { StorageBatchGetCountersResponse } from './storageBatchGetCountersResponse';
import { StorageBatchGetCountersSingleResponse } from './storageBatchGetCountersSingleResponse';
import { StorageBatchGetJsonBlobsRequest } from './storageBatchGetJsonBlobsRequest';
import { StorageBatchGetJsonBlobsResponse } from './storageBatchGetJsonBlobsResponse';
import { StorageBatchGetJsonBlobsSingleResponse } from './storageBatchGetJsonBlobsSingleResponse';
import { StorageBatchGetSubDocumentsRequest } from './storageBatchGetSubDocumentsRequest';
import { StorageBatchGetSubDocumentsResponse } from './storageBatchGetSubDocumentsResponse';
import { StorageBatchGetSubDocumentsSingleResponse } from './storageBatchGetSubDocumentsSingleResponse';
import { StorageBatchIncrementCounterRequest } from './storageBatchIncrementCounterRequest';
import { StorageBatchIncrementCounterResponse } from './storageBatchIncrementCounterResponse';
import { StorageBatchInsertBlobRequest } from './storageBatchInsertBlobRequest';
import { StorageBatchInsertBlobResponse } from './storageBatchInsertBlobResponse';
import { StorageBatchInsertJsonBlobSingleResponse } from './storageBatchInsertJsonBlobSingleResponse';
import { StorageBatchInsertJsonBlobsRequest } from './storageBatchInsertJsonBlobsRequest';
import { StorageBatchInsertJsonBlobsResponse } from './storageBatchInsertJsonBlobsResponse';
import { StorageBatchPrependArrSubDocumentSingleResponse } from './storageBatchPrependArrSubDocumentSingleResponse';
import { StorageBatchPrependArrSubDocumentsRequest } from './storageBatchPrependArrSubDocumentsRequest';
import { StorageBatchPrependArrSubDocumentsResponse } from './storageBatchPrependArrSubDocumentsResponse';
import { StorageBatchReplaceBlobRequest } from './storageBatchReplaceBlobRequest';
import { StorageBatchReplaceBlobResponse } from './storageBatchReplaceBlobResponse';
import { StorageBatchReplaceJsonBlobSingleResponse } from './storageBatchReplaceJsonBlobSingleResponse';
import { StorageBatchReplaceJsonBlobsRequest } from './storageBatchReplaceJsonBlobsRequest';
import { StorageBatchReplaceJsonBlobsResponse } from './storageBatchReplaceJsonBlobsResponse';
import { StorageBatchSingleBlobResponse } from './storageBatchSingleBlobResponse';
import { StorageBatchSingleIncrementCounterResponse } from './storageBatchSingleIncrementCounterResponse';
import { StorageBatchSingleReplaceBlobResponse } from './storageBatchSingleReplaceBlobResponse';
import { StorageBatchSingleUpdateAppendBlobResponse } from './storageBatchSingleUpdateAppendBlobResponse';
import { StorageBatchUpdateAppendBlobRequest } from './storageBatchUpdateAppendBlobRequest';
import { StorageBatchUpdateAppendBlobResponse } from './storageBatchUpdateAppendBlobResponse';
import { StorageBatchUpsertSubDocumentSingleResponse } from './storageBatchUpsertSubDocumentSingleResponse';
import { StorageBatchUpsertSubDocumentsRequest } from './storageBatchUpsertSubDocumentsRequest';
import { StorageBatchUpsertSubDocumentsResponse } from './storageBatchUpsertSubDocumentsResponse';
import { StorageBlobAndOwner } from './storageBlobAndOwner';
import { StorageCounterAndOwner } from './storageCounterAndOwner';
import { StorageDeleteAppendBlobResponse } from './storageDeleteAppendBlobResponse';
import { StorageDeleteBlobResponse } from './storageDeleteBlobResponse';
import { StorageDeleteJsonBlobRequest } from './storageDeleteJsonBlobRequest';
import { StorageDeleteJsonBlobResponse } from './storageDeleteJsonBlobResponse';
import { StorageDeleteSubDocumentRequest } from './storageDeleteSubDocumentRequest';
import { StorageDeleteSubDocumentResponse } from './storageDeleteSubDocumentResponse';
import { StorageGetAppendBlobRequest } from './storageGetAppendBlobRequest';
import { StorageGetAppendBlobResponse } from './storageGetAppendBlobResponse';
import { StorageGetBlobRequest } from './storageGetBlobRequest';
import { StorageGetBlobResponse } from './storageGetBlobResponse';
import { StorageGetCasResponse } from './storageGetCasResponse';
import { StorageGetCounterRequest } from './storageGetCounterRequest';
import { StorageGetCounterResponse } from './storageGetCounterResponse';
import { StorageGetJsonBlobRequest } from './storageGetJsonBlobRequest';
import { StorageGetJsonBlobResponse } from './storageGetJsonBlobResponse';
import { StorageGetSubDocumentRequest } from './storageGetSubDocumentRequest';
import { StorageGetSubDocumentResponse } from './storageGetSubDocumentResponse';
import { StorageIncrementCounterRequest } from './storageIncrementCounterRequest';
import { StorageIncrementCounterResponse } from './storageIncrementCounterResponse';
import { StorageInsertBlobRequest } from './storageInsertBlobRequest';
import { StorageInsertBlobResponse } from './storageInsertBlobResponse';
import { StorageInsertJsonBlobRequest } from './storageInsertJsonBlobRequest';
import { StorageInsertJsonBlobResponse } from './storageInsertJsonBlobResponse';
import { StorageJsonFragment } from './storageJsonFragment';
import { StoragePrependArrSubDocumentRequest } from './storagePrependArrSubDocumentRequest';
import { StoragePrependArrSubDocumentResponse } from './storagePrependArrSubDocumentResponse';
import { StorageReplaceBlobRequest } from './storageReplaceBlobRequest';
import { StorageReplaceBlobResponse } from './storageReplaceBlobResponse';
import { StorageReplaceJsonBlobRequest } from './storageReplaceJsonBlobRequest';
import { StorageReplaceJsonBlobResponse } from './storageReplaceJsonBlobResponse';
import { StorageResetCounterResponse } from './storageResetCounterResponse';
import { StorageUpdateAppendBlobRequest } from './storageUpdateAppendBlobRequest';
import { StorageUpdateAppendBlobResponse } from './storageUpdateAppendBlobResponse';
import { StorageUpsertSubDocumentRequest } from './storageUpsertSubDocumentRequest';
import { StorageUpsertSubDocumentResponse } from './storageUpsertSubDocumentResponse';
import { StorageUserAppendBlobResponse } from './storageUserAppendBlobResponse';
import { StorageUserBlobResponse } from './storageUserBlobResponse';
import { StorageUserCounterResponse } from './storageUserCounterResponse';
import { SuccessResponseSchema } from './successResponseSchema';
import { SuccessResponseSchemaId } from './successResponseSchemaId';
import { SuspendUserRequest } from './suspendUserRequest';
import { UpdateAppendBlobRequest } from './updateAppendBlobRequest';
import { UpsertSubDocumentRequest } from './upsertSubDocumentRequest';

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
        "StorageAppendArrSubDocumentRequest.AccessTypeEnum": StorageAppendArrSubDocumentRequest.AccessTypeEnum,
        "StorageDeleteJsonBlobRequest.AccessTypeEnum": StorageDeleteJsonBlobRequest.AccessTypeEnum,
        "StorageDeleteSubDocumentRequest.AccessTypeEnum": StorageDeleteSubDocumentRequest.AccessTypeEnum,
        "StorageGetAppendBlobRequest.AccessTypeEnum": StorageGetAppendBlobRequest.AccessTypeEnum,
        "StorageGetBlobRequest.AccessTypeEnum": StorageGetBlobRequest.AccessTypeEnum,
        "StorageGetCounterRequest.AccessTypeEnum": StorageGetCounterRequest.AccessTypeEnum,
        "StorageGetJsonBlobRequest.AccessTypeEnum": StorageGetJsonBlobRequest.AccessTypeEnum,
        "StorageGetSubDocumentRequest.AccessTypeEnum": StorageGetSubDocumentRequest.AccessTypeEnum,
        "StorageIncrementCounterRequest.AccessTypeEnum": StorageIncrementCounterRequest.AccessTypeEnum,
        "StorageInsertBlobRequest.AccessTypeEnum": StorageInsertBlobRequest.AccessTypeEnum,
        "StorageInsertJsonBlobRequest.AccessTypeEnum": StorageInsertJsonBlobRequest.AccessTypeEnum,
        "StoragePrependArrSubDocumentRequest.AccessTypeEnum": StoragePrependArrSubDocumentRequest.AccessTypeEnum,
        "StorageReplaceBlobRequest.AccessTypeEnum": StorageReplaceBlobRequest.AccessTypeEnum,
        "StorageReplaceJsonBlobRequest.AccessTypeEnum": StorageReplaceJsonBlobRequest.AccessTypeEnum,
        "StorageUpdateAppendBlobRequest.AccessTypeEnum": StorageUpdateAppendBlobRequest.AccessTypeEnum,
        "StorageUpsertSubDocumentRequest.AccessTypeEnum": StorageUpsertSubDocumentRequest.AccessTypeEnum,
}

let typeMap: {[index: string]: any} = {
    "ApiHttpBody": ApiHttpBody,
    "AppendArrSubDocumentRequest": AppendArrSubDocumentRequest,
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
    "ErrorResponseSchema": ErrorResponseSchema,
    "ErrorResponseSchemaId": ErrorResponseSchemaId,
    "IncrementCounterRequest": IncrementCounterRequest,
    "InsertBlobRequest": InsertBlobRequest,
    "InsertJsonBlobRequest": InsertJsonBlobRequest,
    "MCPRequestSchema": MCPRequestSchema,
    "MCPRequestSchemaId": MCPRequestSchemaId,
    "PrependArrSubDocumentRequest": PrependArrSubDocumentRequest,
    "ProtobufAny": ProtobufAny,
    "ReplaceBlobRequest": ReplaceBlobRequest,
    "ReplaceJsonBlobRequest": ReplaceJsonBlobRequest,
    "StorageAppendArrSubDocumentRequest": StorageAppendArrSubDocumentRequest,
    "StorageAppendArrSubDocumentResponse": StorageAppendArrSubDocumentResponse,
    "StorageAppendBlobAndOwner": StorageAppendBlobAndOwner,
    "StorageBatchAppendArrSubDocumentSingleResponse": StorageBatchAppendArrSubDocumentSingleResponse,
    "StorageBatchAppendArrSubDocumentsRequest": StorageBatchAppendArrSubDocumentsRequest,
    "StorageBatchAppendArrSubDocumentsResponse": StorageBatchAppendArrSubDocumentsResponse,
    "StorageBatchDeleteJsonBlobsRequest": StorageBatchDeleteJsonBlobsRequest,
    "StorageBatchDeleteJsonBlobsResponse": StorageBatchDeleteJsonBlobsResponse,
    "StorageBatchDeleteJsonBlobsSingleResponse": StorageBatchDeleteJsonBlobsSingleResponse,
    "StorageBatchDeleteSubDocumentSingleResponse": StorageBatchDeleteSubDocumentSingleResponse,
    "StorageBatchDeleteSubDocumentsRequest": StorageBatchDeleteSubDocumentsRequest,
    "StorageBatchDeleteSubDocumentsResponse": StorageBatchDeleteSubDocumentsResponse,
    "StorageBatchGetAppendBlobsResponse": StorageBatchGetAppendBlobsResponse,
    "StorageBatchGetAppendBlobsSingleResponse": StorageBatchGetAppendBlobsSingleResponse,
    "StorageBatchGetBlobsResponse": StorageBatchGetBlobsResponse,
    "StorageBatchGetBlobsSingleResponse": StorageBatchGetBlobsSingleResponse,
    "StorageBatchGetCountersResponse": StorageBatchGetCountersResponse,
    "StorageBatchGetCountersSingleResponse": StorageBatchGetCountersSingleResponse,
    "StorageBatchGetJsonBlobsRequest": StorageBatchGetJsonBlobsRequest,
    "StorageBatchGetJsonBlobsResponse": StorageBatchGetJsonBlobsResponse,
    "StorageBatchGetJsonBlobsSingleResponse": StorageBatchGetJsonBlobsSingleResponse,
    "StorageBatchGetSubDocumentsRequest": StorageBatchGetSubDocumentsRequest,
    "StorageBatchGetSubDocumentsResponse": StorageBatchGetSubDocumentsResponse,
    "StorageBatchGetSubDocumentsSingleResponse": StorageBatchGetSubDocumentsSingleResponse,
    "StorageBatchIncrementCounterRequest": StorageBatchIncrementCounterRequest,
    "StorageBatchIncrementCounterResponse": StorageBatchIncrementCounterResponse,
    "StorageBatchInsertBlobRequest": StorageBatchInsertBlobRequest,
    "StorageBatchInsertBlobResponse": StorageBatchInsertBlobResponse,
    "StorageBatchInsertJsonBlobSingleResponse": StorageBatchInsertJsonBlobSingleResponse,
    "StorageBatchInsertJsonBlobsRequest": StorageBatchInsertJsonBlobsRequest,
    "StorageBatchInsertJsonBlobsResponse": StorageBatchInsertJsonBlobsResponse,
    "StorageBatchPrependArrSubDocumentSingleResponse": StorageBatchPrependArrSubDocumentSingleResponse,
    "StorageBatchPrependArrSubDocumentsRequest": StorageBatchPrependArrSubDocumentsRequest,
    "StorageBatchPrependArrSubDocumentsResponse": StorageBatchPrependArrSubDocumentsResponse,
    "StorageBatchReplaceBlobRequest": StorageBatchReplaceBlobRequest,
    "StorageBatchReplaceBlobResponse": StorageBatchReplaceBlobResponse,
    "StorageBatchReplaceJsonBlobSingleResponse": StorageBatchReplaceJsonBlobSingleResponse,
    "StorageBatchReplaceJsonBlobsRequest": StorageBatchReplaceJsonBlobsRequest,
    "StorageBatchReplaceJsonBlobsResponse": StorageBatchReplaceJsonBlobsResponse,
    "StorageBatchSingleBlobResponse": StorageBatchSingleBlobResponse,
    "StorageBatchSingleIncrementCounterResponse": StorageBatchSingleIncrementCounterResponse,
    "StorageBatchSingleReplaceBlobResponse": StorageBatchSingleReplaceBlobResponse,
    "StorageBatchSingleUpdateAppendBlobResponse": StorageBatchSingleUpdateAppendBlobResponse,
    "StorageBatchUpdateAppendBlobRequest": StorageBatchUpdateAppendBlobRequest,
    "StorageBatchUpdateAppendBlobResponse": StorageBatchUpdateAppendBlobResponse,
    "StorageBatchUpsertSubDocumentSingleResponse": StorageBatchUpsertSubDocumentSingleResponse,
    "StorageBatchUpsertSubDocumentsRequest": StorageBatchUpsertSubDocumentsRequest,
    "StorageBatchUpsertSubDocumentsResponse": StorageBatchUpsertSubDocumentsResponse,
    "StorageBlobAndOwner": StorageBlobAndOwner,
    "StorageCounterAndOwner": StorageCounterAndOwner,
    "StorageDeleteAppendBlobResponse": StorageDeleteAppendBlobResponse,
    "StorageDeleteBlobResponse": StorageDeleteBlobResponse,
    "StorageDeleteJsonBlobRequest": StorageDeleteJsonBlobRequest,
    "StorageDeleteJsonBlobResponse": StorageDeleteJsonBlobResponse,
    "StorageDeleteSubDocumentRequest": StorageDeleteSubDocumentRequest,
    "StorageDeleteSubDocumentResponse": StorageDeleteSubDocumentResponse,
    "StorageGetAppendBlobRequest": StorageGetAppendBlobRequest,
    "StorageGetAppendBlobResponse": StorageGetAppendBlobResponse,
    "StorageGetBlobRequest": StorageGetBlobRequest,
    "StorageGetBlobResponse": StorageGetBlobResponse,
    "StorageGetCasResponse": StorageGetCasResponse,
    "StorageGetCounterRequest": StorageGetCounterRequest,
    "StorageGetCounterResponse": StorageGetCounterResponse,
    "StorageGetJsonBlobRequest": StorageGetJsonBlobRequest,
    "StorageGetJsonBlobResponse": StorageGetJsonBlobResponse,
    "StorageGetSubDocumentRequest": StorageGetSubDocumentRequest,
    "StorageGetSubDocumentResponse": StorageGetSubDocumentResponse,
    "StorageIncrementCounterRequest": StorageIncrementCounterRequest,
    "StorageIncrementCounterResponse": StorageIncrementCounterResponse,
    "StorageInsertBlobRequest": StorageInsertBlobRequest,
    "StorageInsertBlobResponse": StorageInsertBlobResponse,
    "StorageInsertJsonBlobRequest": StorageInsertJsonBlobRequest,
    "StorageInsertJsonBlobResponse": StorageInsertJsonBlobResponse,
    "StorageJsonFragment": StorageJsonFragment,
    "StoragePrependArrSubDocumentRequest": StoragePrependArrSubDocumentRequest,
    "StoragePrependArrSubDocumentResponse": StoragePrependArrSubDocumentResponse,
    "StorageReplaceBlobRequest": StorageReplaceBlobRequest,
    "StorageReplaceBlobResponse": StorageReplaceBlobResponse,
    "StorageReplaceJsonBlobRequest": StorageReplaceJsonBlobRequest,
    "StorageReplaceJsonBlobResponse": StorageReplaceJsonBlobResponse,
    "StorageResetCounterResponse": StorageResetCounterResponse,
    "StorageUpdateAppendBlobRequest": StorageUpdateAppendBlobRequest,
    "StorageUpdateAppendBlobResponse": StorageUpdateAppendBlobResponse,
    "StorageUpsertSubDocumentRequest": StorageUpsertSubDocumentRequest,
    "StorageUpsertSubDocumentResponse": StorageUpsertSubDocumentResponse,
    "StorageUserAppendBlobResponse": StorageUserAppendBlobResponse,
    "StorageUserBlobResponse": StorageUserBlobResponse,
    "StorageUserCounterResponse": StorageUserCounterResponse,
    "SuccessResponseSchema": SuccessResponseSchema,
    "SuccessResponseSchemaId": SuccessResponseSchemaId,
    "SuspendUserRequest": SuspendUserRequest,
    "UpdateAppendBlobRequest": UpdateAppendBlobRequest,
    "UpsertSubDocumentRequest": UpsertSubDocumentRequest,
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
