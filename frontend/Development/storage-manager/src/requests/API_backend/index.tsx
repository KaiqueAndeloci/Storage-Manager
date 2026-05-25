'use server'
import { formResponse } from '@/interfaces/index'
import { NextResponse } from "next/server";
import { cookies } from 'next/headers';
import { isKeyObject } from 'util/types';


const URL_BASE = 'http://127.0.0.1:8001'

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
        request = await requestAPI({
            url: `${URL_BASE}/users/me`,
            method: 'GET',
            token: request.response_api.access
        })
    }
    if (request.response_api.access != undefined && request.response_api.access != null) {
        const maxAge1 = 60 * 60 * 24 * 29; // 29 dias
        const maxAge2 = 60 * 4; // 4 min

        (await cookies()).set({
            name: 'Name',
            value: request.response_api.Name,
            httpOnly: true,
            secure: true,
            sameSite: 'strict',
            path: '/',
            maxAge: maxAge1,
        });
        (await cookies()).set({
            name: 'user_email',
            value: request.response_api.email,
            httpOnly: true,
            secure: true,
            sameSite: 'strict',
            path: '/',
            maxAge: maxAge1,
        });
        (await cookies()).set({
            name: 'user_permission',
            value: request.response_api.User_type,
            httpOnly: true,
            secure: true,
            sameSite: 'strict',
            path: '/',
            maxAge: maxAge1,
        });
        (await cookies()).set({
            name: 'Date_creation',
            value: request.response_api.Date_creation,
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
    else {

        return {
            success: false, response_api: request.response_api
        }
    }
}

export async function logoutAction():
    Promise<formResponse> {
    (await cookies()).set({
        name: 'user_name',
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
        name: 'date_creation',
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