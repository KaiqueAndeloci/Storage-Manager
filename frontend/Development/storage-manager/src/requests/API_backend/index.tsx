'use server'
import { formResponse } from '@/Interfaces/index'
import { NextResponse } from "next/server";
import { cookies } from 'next/headers';
import { isKeyObject } from 'util/types';


const URL_BASE = 'http://127.0.0.1:8000'

function requestOptions({ body, method, token = undefined }: { body?: object, method: string, token?: string }) {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    if (token) {
        myHeaders.append("Authorization", "Bearer " + token);
    }

    const raw = JSON.stringify(
        body
    );

    const requestOptions = {
        method: method,
        headers: myHeaders,
        body: raw,
        redirect: undefined
    };
    return requestOptions
}

export async function requestAPI({ url, body, method, token = undefined }: { url: string, body?: object, method: string, token?: string }):
    Promise<formResponse> {
    await new Promise(r => setTimeout(r, 1500))

    const response = await fetch(`${url}`, requestOptions(
        {
            body: body,
            token: token,
            method: method
        }
    )).then((response) => { return { success: true, message: response.json() } }).catch((err) => {
        return { success: false, message: err };
    })

    if (response.success === true) {
        return { success: true, response_api: await response.message }
    } else {
        return { success: false, response_api: await response.message }
    }

}

export async function loginAction({ user, password }: { user: string, password: string }):
    Promise<formResponse> {
    let request = await requestAPI({
        url: `${URL_BASE}/authentication/token`,
        body: { 'username': user, 'pw': password }, method: 'POST'
    })

    if (request.response_api.access != undefined && request.response_api.access != null) {
        const request_me = await requestAPI({
            url: `${URL_BASE}/users/me`,
            method: 'GET',
            token: request.response_api.access
        })

        if (request_me.response_api.Name != undefined && request_me.response_api.Name != null) {
            const maxAge1 = 60 * 60 * 24 * 29; // 29 dias
            const maxAge2 = 60 * 4; // 4 min

            (await cookies()).set({
                name: 'access',
                value: request.response_api.access,
                httpOnly: true,
                secure: true,
                sameSite: 'strict',
                path: '/',
                maxAge: maxAge1,
            });

            (await cookies()).set({
                name: 'refresh',
                value: request.response_api.refresh,
                httpOnly: true,
                secure: true,
                sameSite: 'strict',
                path: '/',
                maxAge: maxAge1,
            });

            (await cookies()).set({
                name: 'Name',
                value: request_me.response_api.Name,
                httpOnly: true,
                secure: true,
                sameSite: 'strict',
                path: '/',
                maxAge: maxAge1,
            });
            (await cookies()).set({
                name: 'user_email',
                value: request_me.response_api.email,
                httpOnly: true,
                secure: true,
                sameSite: 'strict',
                path: '/',
                maxAge: maxAge1,
            });
            (await cookies()).set({
                name: 'user_permission',
                value: request_me.response_api.UserType,
                httpOnly: true,
                secure: true,
                sameSite: 'strict',
                path: '/',
                maxAge: maxAge1,
            });
            (await cookies()).set({
                name: 'Date_creation',
                value: request_me.response_api.Date_creation,
                httpOnly: true,
                secure: true,
                sameSite: 'strict',
                path: '/',
                maxAge: maxAge1,
            });

            return {
                success: true, response_api: request.response_api
            }
        }
    }

    return {
        success: false, response_api: request.response_api
    }
}

export async function logoutAction():
    Promise<formResponse> {
    (await cookies()).set({
        name: 'Name',
        value: ``,
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        path: '/',
        maxAge: 0,
    });
    (await cookies()).set({
        name: 'user_email',
        value: ``,
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        path: '/',
        maxAge: 0,
    });
    (await cookies()).set({
        name: 'user_permission',
        value: ``,
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        path: '/',
        maxAge: 0,
    });
    (await cookies()).set({
        name: 'Date_creation',
        value: ``,
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        path: '/',
        maxAge: 0,
    });
    (await cookies()).set({
        name: 'refresh',
        value: ``,
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        path: '/',
        maxAge: 0,
    });
    (await cookies()).set({
        name: 'access',
        value: ``,
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        path: '/',
        maxAge: 0,
    });

    return {
        success: true, response_api: 'Success'
    }
};

export async function getUsersAction({ Limit, Offset }: { Limit: number, Offset: number }): Promise<formResponse> {
    const access_token = (await cookies()).get("access")
    //.then((value)=>{return value?.value || undefined}).catch((value)=>{return undefined});

    let request = await requestAPI({
        url: `${URL_BASE}/users?Limit=${Limit}&Offset=${Offset}&OrderBy=ID`,
        body: undefined, method: 'GET',
        token: access_token?.value
    })

    if (request.response_api.Users != undefined && request.response_api.Users != null) {
        return {
            success: true, response_api: request.response_api
        }
    }

    return {
        success: false, response_api: request.response_api
    }
}