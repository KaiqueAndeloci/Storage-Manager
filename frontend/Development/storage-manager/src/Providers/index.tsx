'use client'
import React, { createContext, useContext, useState, useEffect, use } from 'react';
import { AuthenticateContext, user, permission_type, page } from "@/Interfaces/index"
// import { usePathname } from 'next/navigation'
// import routes from '@/app/routes'
// import { logoutAction, loginAction } from '@/requests/API_backend';


const AuthContext = createContext<AuthenticateContext>({
    user_details: undefined,
    setPage: async (page: page) => { },
    logout: async () => { }
})

export const AuthProvider = ({ children, user }: { children: React.ReactNode, user: user | undefined; }) => {
    const [pageState, setPageState] = useState<page | undefined>(undefined)
    // const [userState, setUser] = useState<user | undefined>(undefined)
    // const protectedRoutes = [routes.pages]
    // const loginPage = [routes.login]
    // const pathname = usePathname()

    // const isProtected = protectedRoutes.some(route =>
    //     pathname.includes(route)
    // )

    // const isLoginPage = loginPage.some(route =>
    //     pathname.includes(route)
    // )

    // if (isProtected && !isLoginPage) {
    //     const user_cookies = getUserCookies()
    //     if (user_cookies.UserEmail && user_cookies.UserName && user_cookies.UserPermission && user_cookies.date_creation) {
    //         if (user_cookies.UserPermission === 'ADMIN' || user_cookies.UserPermission === 'cashier' || user_cookies.UserPermission === 'logistic') {
    //             setUser({ name: user_cookies.UserName, email: user_cookies.UserEmail, permission_type: user_cookies.UserPermission, date_creation: user_cookies.date_creation })
    //         }
    //     }
    // }

    // function getUserCookies() {
    //     return {
    //         UserName: "getCookie('UserName')",
    //         UserEmail: "getCookie('UserEmail')",
    //         UserPermission: "ADMIN",
    //         date_creation: "getCookie('date_creation')"
    //     }
    // }
    async function setPage() {

    }

    async function login(name: string, email: string, userPermission: permission_type) {

        // const dataExpiracao = new Date();
        // dataExpiracao.setTime(dataExpiracao.getTime() + (1000 * 60 * 60 * 24 * 29));
        // const expires = "expires=" + dataExpiracao.toUTCString();
        // document.cookie = `UserName=${decodeURIComponent(name)}; ${expires}; path=/`;
        // document.cookie = `UserEmail=${decodeURIComponent(email)}; ${expires}; path=/`;
        // document.cookie = `UserPermission=${userPermission}; ${expires}; path=/`;
        // setUser({ name: name, date_creation: '', email: email, permission_type: userPermission })
    }

    async function logout() {
        // await logoutAction()
    }

    return (
        <AuthContext.Provider value={{
            user_details: user,
            page: pageState,
            setPage: setPageState,
            logout,
        }}>
            {children}
        </AuthContext.Provider>
    )
}


export const useAuth = () => use(AuthContext);