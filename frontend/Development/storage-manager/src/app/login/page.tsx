'use server'
import { LoginForm } from "@/components/custom/forms/login"
import { Suspense } from "react"
import Loading from '@/app/loading'


export default async function Login() {
    return (
        <Suspense fallback={<Loading></Loading>}>
            <LoginForm></LoginForm>
        </Suspense>
    )
}