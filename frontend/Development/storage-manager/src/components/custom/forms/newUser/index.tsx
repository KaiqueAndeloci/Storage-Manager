"use client"
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from '@/components/ui/label';
import { Suspense, use, useState } from "react";
import { createUserAction } from '@/requests/API_backend/index'
import { Notify } from "@/components/custom/notification/index";
import { ButtonSubmit } from "@/components/custom/button";
import { redirect } from 'next/navigation'
import { routes } from '@/app/routes'
import { RadioButton } from "@/components/custom/input/radioButton/index"

export function UserForm() {
    const [show, setShow] = useState(false);
    const [radioState, setRadioState] = useState("ADMIN");
    const url = routes.management //`${routes.management}?Notify=${encodeURIComponent("Usuário criado")}`

    const handleUser: React.ComponentProps<"form">["onSubmit"] = async (e) => {
        e.preventDefault();
        const target = e.currentTarget
        const formData = new FormData(target);
        const name = `${formData.get('name')}`
        const user = `${formData.get('username')}`
        const password = `${formData.get('password')}`
        const email = `${formData.get('email')}`
        const UserType = `${formData.get('UserType')}`
        const PhoneNumber = `${formData.get('PhoneNumber')}`
        const DDDNumber = `${formData.get('DDDNumber')}`
        const WorkPosition = `${formData.get('WorkPosition')}`
        const LeaderEmail = `${formData.get('LeaderEmail')}`
        let body = undefined

        if (!name || !user || !password || !email || !UserType) {
            Notify({ message: 'Preencha todos os campos!', message_type: 'ERROR' })
        } else if (UserType === "cashier" || UserType === "logistic") {
            if (!PhoneNumber || !DDDNumber || !WorkPosition || !LeaderEmail) {
                Notify({ message: 'Preencha todos os campos!', message_type: 'ERROR' })
            } else {
                body = { name: name, user: user, password: password, email: email, userType: UserType, DDDNumber: Number(DDDNumber), PhoneNumber: Number(DDDNumber), LeaderEmail: LeaderEmail, WorkPosition: WorkPosition }
            }
        } else {
            body = { name: name, user: user, password: password, email: email, userType: UserType }
        }

        if (body) {
            const response = await createUserAction(body)
            console.log(response)
            if (response.success === true) {
                Notify({ message: `Usuário criado`, message_type: 'SUCCESS' })
                // target.reset()
                // redirect(url)
            }
            else {
                Notify({ message: 'Erro na criação desse usuário', message_type: 'ERROR' })
            }
        }
    }

    // className="text-white flex flex-col gap-3 min-w-sm mr-6 ml-6 sm:mr-16 sm:ml-16 md:mr-24 md:ml-24 lg:mr-auto lg:ml-auto lg:w-lg"

    return (
        <form onSubmit={handleUser} className="grid flex-1 auto-rows-min gap-6 px-4">
            <p>Please, fill all inputs below</p>
            <div className="grid gap-3">
                <Input className="text-black" maxLength={100} name={'name'} type="text" placeholder="Name" />
            </div>
            <div className="grid gap-3">
                <Input className="text-black" maxLength={100} name={'username'} type="text" placeholder="Username" />
            </div>
            <div className="grid gap-3">
                <Input className="text-black" maxLength={100} name={'password'} type={show ? 'text' : 'password'} placeholder="Password" />
                <div className="w-full flex gap-4">
                    <Checkbox onCheckedChange={() => { setShow(!show) }} id="pass"></Checkbox>
                    <Label htmlFor="pass" className="text-black">Show password</Label>
                </div>
            </div>
            <div className="grid gap-3">
                <Input className="text-black" maxLength={100} name={'email'} type="email" placeholder="Email" />
            </div>
            <div>
                <RadioButton
                    name="UserType"
                    label={["ADMIN", "cashier", "logistic"]}
                    getChecked={setRadioState}
                    optionChecked={radioState}
                ></RadioButton>
            </div>
            <div className="grid gap-3" hidden={radioState === "cashier" || radioState === "logistic" ? false : true}>
                <Input className="text-black" maxLength={100} name={'PhoneNumber'} type="number" placeholder="Phone number" />
            </div>
            <div className="grid gap-3" hidden={radioState === "cashier" || radioState === "logistic" ? false : true}>
                <Input className="text-black" maxLength={4} name={'DDDNumber'} type="number" placeholder="DDD" />
            </div>
            <div className="grid gap-3" hidden={radioState === "cashier" || radioState === "logistic" ? false : true}>
                <Input className="text-black" maxLength={100} name={'WorkPosition'} type="text" placeholder="Work Position" />
            </div>
            <div className="grid gap-3" hidden={radioState === "cashier" || radioState === "logistic" ? false : true}>
                <Input className="text-black" maxLength={100} name={'LeaderEmail'} type="email" placeholder="Leader email" />
            </div>

            <ButtonSubmit />
        </form>
    )
}



