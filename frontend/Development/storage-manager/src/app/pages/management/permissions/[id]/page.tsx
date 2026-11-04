'use server'
import { RenderFields } from "@/components/custom/util/index"
import { fieldModel } from "@/Interfaces"
import { transferItem } from '@/Interfaces/index'
import { SimpleForm } from '@/components/custom/forms/SimpleForm'
import { SubmitEvent } from "react";
import { Notify } from "@/components/custom/notification/index";
import { editUserAction, createUserAction, getUserAction } from '@/requests/API_backend/index'
import { redirect } from 'next/navigation'
import { routes } from '@/app/routes'
import { TablePermissionActions } from '@/components/custom/tables/permissions/index'
import { Suspense } from "react"
import Loading from '@/app/loading'
import { getGroupsAction, getGroupPermissionsAction, getPermissionsAction } from '@/requests/API_backend/index'


interface PageProps {

    searchParams: Promise<{
        id: string;
        Limit?: string;
        Offset?: string;
    }>;
}

export default async function UserPermissions({
    searchParams,
}: PageProps) {
    const params = await searchParams;
    const Limit = Number(params.Limit || 10);
    const Offset = Number(params.Offset || 0);
    const id = Number(params.id || 0)
    let response_groups = getGroupsAction({ Limit: Limit, Offset: Offset })
    let response_group = await getGroupPermissionsAction({ IDuser: 1, Limit: Limit, Offset: Offset })
    const response_permissions = await getPermissionsAction({ Limit: Limit, Offset: Offset })
    let total = 0;
    let available: transferItem[] = []
    let selected: transferItem[] = []

    let counter = 0;
    if (response_group.success === true && response_permissions.success === true) {
        for (let index = 0; index < response_group.response_api.GroupsDetails.length; index++) {
            for (let index2 = 0; index2 < response_group.response_api.GroupsDetails[index].Permissions.length; index2++) {
                counter++;
                selected.push(
                    {
                        id: `${counter}`,
                        label: `${response_group.response_api.GroupsDetails[index].Permissions[index2].Permission_name
                            } (${response_group.response_api.GroupsDetails[index].Permissions[index2].Permission_type})`
                    }
                )

            }
        }
        if (response_group.response_api.Total !== undefined && response_group.response_api.Total !== null) {
            total = response_group.response_api.Total
        }
    }
    // {
    // "GroupsDetails": [
    //     {
    //     "IDGroup": 1,
    //     "Permissions": [
    //         {

    const url = routes.management
    // const teste: transferItem[] = [
    //     { id: "1", label: "Visualizar usuários" },
    //     { id: "2", label: "Criar usuários" },
    //     { id: "3", label: "Editar usuários" },
    //     { id: "4", label: "Excluir usuários" },
    //     { id: "5", label: "Gerenciar grupos" },
    // ]

    const id_formated = Number(`${id}`)
    const fields: fieldModel[] = [
        {
            className: "text-black",
            hidden: false,
            maxLength: 100,
            name: "Name",
            placeholder: "Name",
            defaultValue: "",
            type: "text"
        },
        {
            className: "text-black",
            hidden: false,
            maxLength: 100,
            name: "Email",
            placeholder: "Email",
            defaultValue: "",
            type: "text"
        },
        {
            className: "text-black",
            hidden: false,
            maxLength: 100,
            name: "UserType",
            placeholder: "User Type",
            defaultValue: "",
            type: "text"
        },
        {
            className: "text-black",
            hidden: false,
            maxLength: 100,
            name: "PermissõesAtuais",
            placeholder: "Permissões Atuais",
            defaultValue: "",
            transferListProps: { available: available, selected: selected },
            type: "dual-listbox"
        },
    ]


    return (
        <Suspense fallback={<Loading></Loading>}>
            <TablePermissionActions fields={fields} Limit={1} Offset={1} Total={1} headers={[]}></TablePermissionActions>
        </Suspense>
    )
}