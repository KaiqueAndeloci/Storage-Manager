'use client'
import { RenderFields } from "@/components/custom/util/index"
import { fieldModel, Users_table } from "@/Interfaces"
import { transferItem } from '@/Interfaces/index'
import { SimpleForm } from '@/components/custom/forms/SimpleForm'
import { SubmitEvent } from "react";
import { Notify } from "@/components/custom/notification/index";
import { editUserAction, createUserAction, getUserAction } from '@/requests/API_backend/index'
import { redirect } from 'next/navigation'
import { routes } from '@/app/routes'

export function TablePermissionActions({
    fields, headers, Total, Limit, Offset
}: {
    fields: fieldModel[], headers: string[], Total: number, Limit: number, Offset: number
}) {
    const url = routes.management
    const handleUpdateUser = async (e: SubmitEvent<HTMLFormElement>) => {
        e.preventDefault();
        const target = e.currentTarget
        const formData = new FormData(target);
        const name = `${formData.get('Name')}`
        const user = `${formData.get('Username')}`
        const password = `${formData.get('Password')}`
        const email = `${formData.get('Email')}`
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
                target.reset()
                redirect(url)
            }
            else {

                Notify({ message: 'Erro na criação desse usuário', message_type: 'ERROR' })
            }
        }
    }
    return (
        <div className="flex flex-col gap-4 text-white">

            <SimpleForm
                title="Please, fill all inputs below"
                fields={fields}
                handleUser={handleUpdateUser}>
            </SimpleForm>
        </div>
    )
}