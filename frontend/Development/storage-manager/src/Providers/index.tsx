'use client'
import React, { createContext, useContext, useState, useEffect } from 'react';
import { AuthenticateContext } from "@/Interfaces/index"

const AuthContext = createContext<AuthenticateContext>({
    login: () => {
    },
    logout: () => { },
})

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    return (
        <AuthContext.Provider value={{

        }}>
            {children}
        </AuthContext.Provider>
    )
}


export const useAuth = () => useContext(AuthContext);