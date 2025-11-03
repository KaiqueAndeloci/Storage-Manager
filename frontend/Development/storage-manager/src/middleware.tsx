'use server'
import { NextRequest, NextResponse } from 'next/server';
import routes from '@/app/routes'


export function middleware(request: NextRequest) {
    const protectedRoutes = [routes.pages]
    const loginPage = [routes.login]
    const { pathname } = request.nextUrl
    const user = request.cookies.get('user_email')?.value

    const isProtected = protectedRoutes.some(route =>
        pathname.includes(route)
    )

    if (isProtected && !user) {
        const loginUrl = new URL(routes.login, request.url)
        loginUrl.searchParams.set('redirect', pathname)
        return NextResponse.redirect(loginUrl)
    }

    const isLoginPage = loginPage.some(route =>
        pathname.includes(route)
    )

    if (isLoginPage && user) {
        return NextResponse.redirect(new URL(routes.dashboard, request.url))
    }


    return NextResponse.next()
}
