"use client"
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from '@/components/ui/label';
import { Suspense, use, useState } from "react";
import { loginAction } from '@/requests/API_backend/index'
import { useAuth } from "@/providers";
import { Notify } from "@/components/custom/notification/index";
import { ButtonSubmit } from "@/components/custom/button";
import { redirect } from 'next/navigation'
import { useSearchParams } from 'next/navigation'
import routes from '@/app/routes'


export function LoginForm() {
    const [show, setShow] = useState(false);
    const context = useAuth()
    const params = useSearchParams()
    const from = params.get('redirect') || routes.dashboard


    async function handleLogin(formData: FormData) {
        const user = `${formData.get('username')}`
        const password = `${formData.get('password')}`


        if (!user || !password) {
            Notify({ message: 'Preencha todos os campos!', message_type: 'ERROR' })
        } else {
            const response = await loginAction({ user: user, password: password })
            console.log(response.success)
            if (user === 'a') {
                Notify({ message: `Bem vindo User`, message_type: 'SUCCESS' })
                // context.login("Kaique", "kaique.andeloci@hotmail.com", "ADMIN")
                redirect(from)
            }
            else {
                Notify({ message: 'Credenciais inválidas', message_type: 'ERROR' })
            }
        }
    }

    return (
        <form action={handleLogin} className="text-white flex flex-col gap-3 min-w-sm mr-6 ml-6 sm:mr-16 sm:ml-16 md:mr-24 md:ml-24 lg:mr-auto lg:ml-auto lg:w-lg">
            <Input maxLength={5} name={'username'} type="text" placeholder="Username" />
            <Input maxLength={5} name={'password'} type={show ? 'text' : 'password'} placeholder="Password" />
            <div className="w-full flex gap-4">
                <Checkbox onCheckedChange={() => { setShow(!show) }} id="pass"></Checkbox>
                <Label htmlFor="pass" className="text-white">Show password</Label>
            </div>
            <ButtonSubmit />
        </form>
    )
}