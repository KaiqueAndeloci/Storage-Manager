'use client'

import { redirect, useRouter } from 'next/navigation'
import { useSearchParams } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Suspense } from "react";
import Loading from '@/app/loading'

import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Checkbox } from "@/components/ui/checkbox";
import { useState } from "react";
import { Users_table, Edit_User } from "@/Interfaces/index"
import { useAuth } from '@/Providers/index'
import { routes } from '@/app/routes'
import { UserForm } from '@/components/custom/forms/newUser'
import { SimpleForm2 } from '@/components/custom/forms/SimpleForm2'
import { DialogDemo } from "@/components/custom/dialog"
import { CardDemo } from "@/components/custom/cards"
import { SimpleForm } from '@/components/custom/forms/SimpleForm'
import { SheetDemo } from "@/components/custom/sheets/newUser"
import { Notify } from "@/components/custom/notification/index";
import { editUserAction, createUserAction, getUserAction } from '@/requests/API_backend/index'
import { fieldModel } from "@/Interfaces"
import { SubmitEvent } from "react";
import { useTransition, useActionState } from 'react';

export function TableActions({
    users, headers, Total, Limit, Offset
}: {
    users: Users_table[], headers: string[], Total: number, Limit: number, Offset: number
}) {
    const auth = useAuth()
    const router = useRouter()
    const previousButton = 0 < Offset ? false : true
    const nextButton = Limit + Offset < Total ? false : true
    const params = useSearchParams()
    const LimitParam = params.get('Limit') || Limit
    const OffsetParam = params.get('Offset') || Offset
    const hasSelected = users.some(user => user.checked);
    const [selectedUsers, setSelectedUsers] = useState<Set<number>>(new Set());
    const [selectedUser, setSelectedUser] = useState<Edit_User | null>(null);
    const [editSheetOpen, setEditSheetOpen] = useState(false);
    const [radioState, setRadioState] = useState<string>("ADMIN");
    const [radioState2, setRadioState2] = useState<string>("ADMIN");
    const [isPending, startTransition] = useTransition();
    const url = routes.management
    const url_permissions = routes.managementPermissions


    const handleClickTransition = (functionExec: () => void) => {
        startTransition(() => {
            functionExec()
        })
    }

    const handleEditClick = async () => {
        if (selectedUser === null) {
            return;
        }

        // Abre o Sheet imediatamente
        setEditSheetOpen(true);
        setRadioState2(selectedUser?.UserType)

        try {
            const response = await getUserAction({ id: selectedUser.ID });
            //response.response_api.
            console.log(response)
            //setSelectedUser({ ID: 0, checked: false, DateCreation: "aaaaaa", Name: "aaaaa", UserType: "ADMIN", DDD_Number: 123, 
            // email: "aaaa@aaa.com.br", Leader_Email: "aaaa@aaa.com.br", Phone_Number: 123, Work_Position: "aaaaa" });
            if (response.success) {
                setSelectedUser({
                    ID: response.response_api.ID,
                    checked: true,
                    DateCreation: response.response_api.DateCreation,
                    Name: response.response_api.Name,
                    UserType: response.response_api.UserType,
                    DDD_Number: response.response_api.DDDNumber,
                    email: response.response_api.Email,
                    Leader_Email: response.response_api.LeaderEmail,
                    Phone_Number: response.response_api.PhoneNumber,
                    Work_Position: response.response_api.WorkPosition
                });
            }
        } catch (error) {
            console.error("Erro ao buscar usuário:", error);
        }

    };

    function toggleUser(user: Users_table, checked: boolean) {
        if (checked) {
            setSelectedUser(user);
        } else {
            setSelectedUser(null);
        }
        setSelectedUsers(prev => {
            const next = new Set(prev);

            if (checked) {
                next.add(user.ID);
            } else {
                next.delete(user.ID);
            }

            return next;
        });
    }

    function HeaderCheckedHandle(checked: boolean | "indeterminate") {
        if (checked === true) {
            setSelectedUsers(new Set(users.map(user => user.ID)));
        } else {
            setSelectedUsers(new Set());
        }
    }

    const handleTestNewUser = async (e: SubmitEvent<HTMLFormElement>) => {
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

    const handleEditUser = async (e: SubmitEvent<HTMLFormElement>) => {
        e.preventDefault();
        const target = e.currentTarget
        const formData = new FormData(target);
        const name = `${formData.get('Name')}`
        const user = `${formData.get('UserName')}`
        const email = `${formData.get('Email')}`
        const date_creation = `${formData.get('DateCreation')}`
        const phone_number = `${formData.get('PhoneNumber')}`
        const DDD_number = `${formData.get('DDDNumber')}`
        const work_position = `${formData.get('WorkPosition')}`
        const leader_email = `${formData.get('LeaderEmail')}`
        const user_type = `${formData.get('UserType')}`
        let body = undefined
        const ID = selectedUser?.ID

        if (!name || !user || !email || !date_creation || !phone_number || !DDD_number || !work_position || !leader_email || !user_type) {
            Notify({ message: 'Preencha todos os campos!', message_type: 'ERROR' })
        } else {
            body = {
                name: name,
                user: "aaaaaaaaaaaaaaaaaaaaaaaa",
                PW: "aaaaaaaaaaaaaaaaaaaaaaaa",
                email: email,
                Date_creation: date_creation,
                PhoneNumber: Number(phone_number),
                DDDNumber: Number(DDD_number),
                WorkPosition: work_position,
                ID: ID ? ID : -1,
                LeaderEmail: leader_email,
                User_type: user_type
            }
        }

        if (body) {
            const response = await editUserAction(body)

            console.log(response)
            if (response.success === true) {
                Notify({ message: `Usuário editado`, message_type: 'SUCCESS' })
                //target.reset()
                //redirect(url)
            }
            else {
                Notify({ message: 'Erro na edição desse usuário', message_type: 'ERROR' })
            }
        }
    }

    const EditUserFields: fieldModel[] = [
        {
            className: "text-black",
            hidden: false,
            maxLength: 100,
            name: "Name",
            placeholder: "Name",
            defaultValue: selectedUser?.Name,
            type: "text"
        },
        // {
        //     className: "text-black",
        //     hidden: false,
        //     maxLength: 100,
        //     name: "UserName",
        //     placeholder: "Username",
        //     defaultValue: selectedUser?.Name,
        //     type: "text"
        // },
        {
            className: "text-black",
            hidden: false,
            maxLength: 100,
            name: "Email",
            placeholder: "Email",
            defaultValue: selectedUser?.email,
            type: "email"
        },
        {
            className: "text-black",
            hidden: false,
            maxLength: 100,
            name: "UserType",
            label: ["ADMIN", "cashier", "logistic"],
            placeholder: "User Type",
            //defaultValue: selectedUser?.UserType,
            setRadioState: setRadioState2,
            radioState: radioState2,
            type: "radio"
        },
        {
            className: "text-black",
            hidden: radioState2 === "cashier" || radioState2 === "logistic" ? false : true,
            maxLength: 100,
            name: "PhoneNumber",
            placeholder: "Phone Number",
            defaultValue: selectedUser?.Phone_Number,
            type: "number"
        },
        {
            className: "text-black",
            hidden: radioState2 === "cashier" || radioState2 === "logistic" ? false : true,
            maxLength: 100,
            name: "DDDNumber",
            placeholder: "DDD Number",
            defaultValue: selectedUser?.DDD_Number,
            type: "number"
        },
        {
            className: "text-black",
            hidden: radioState2 === "cashier" || radioState2 === "logistic" ? false : true,
            maxLength: 100,
            name: "WorkPosition",
            placeholder: "Work Position",
            defaultValue: selectedUser?.Work_Position,
            type: "text"
        },
        {
            className: "text-black",
            hidden: radioState2 === "cashier" || radioState2 === "logistic" ? false : true,
            maxLength: 100,
            name: "LeaderEmail",
            placeholder: "Leader Email",
            defaultValue: selectedUser?.Leader_Email,
            type: "email"
        }
        // name: name,
        // user: "aaaaaaaaaaaaaaaaaaaaaaaa",
        // PW: "aaaaaaaaaaaaaaaaaaaaaaaa",
        // email: email,
        // Date_creation: date_creation,
        // PhoneNumber: Number(phone_number),
        // DDDNumber: Number(DDD_number),
        // WorkPosition: work_position,
        // ID: ID ? ID : -1,
        // LeaderEmail: leader_email,
        // User_type: user_type
    ]

    const NewUserFields: fieldModel[] = [
        {
            className: "text-black",
            hidden: false,
            maxLength: 100,
            name: "Name",
            placeholder: "Name",
            defaultValue: undefined,
            type: "text"
        },
        {
            className: "text-black",
            hidden: false,
            maxLength: 100,
            name: "Username",
            placeholder: "Username",
            defaultValue: undefined,
            type: "text"
        },
        {
            className: "text-black",
            hidden: false,
            maxLength: 100,
            name: "Password",
            placeholder: "Password",
            defaultValue: undefined,
            type: "password"
        },
        {
            className: "text-black",
            hidden: false,
            maxLength: 100,
            name: "Email",
            placeholder: "Email",
            defaultValue: undefined,
            type: "email"
        },
        {
            className: "text-black",
            hidden: false,
            maxLength: 100,
            name: "UserType",
            label: ["ADMIN", "cashier", "logistic"],
            placeholder: "User Type",
            setRadioState: setRadioState,
            radioState: radioState,
            type: "radio"
        },
        {
            className: "text-black",
            hidden: radioState === "cashier" || radioState === "logistic" ? false : true,
            maxLength: 100,
            name: "PhoneNumber",
            placeholder: "Phone number",
            defaultValue: undefined,
            type: "number"
        },
        {
            className: "text-black",
            hidden: radioState === "cashier" || radioState === "logistic" ? false : true,
            maxLength: 100,
            name: "DDDNumber",
            placeholder: "DDD number",
            defaultValue: undefined,
            type: "number"
        },
        {
            className: "text-black",
            hidden: radioState === "cashier" || radioState === "logistic" ? false : true,
            maxLength: 100,
            name: "WorkPosition",
            placeholder: "Work Position",
            defaultValue: undefined,
            type: "text"
        },
        {
            className: "text-black",
            hidden: radioState === "cashier" || radioState === "logistic" ? false : true,
            maxLength: 100,
            name: "Leaderemail",
            placeholder: "Leader email",
            defaultValue: undefined,
            type: "email"
        }
    ]

    return (
        <div className="bg-white p-5 border-2 border-b-gray-50 rounded-md">
            <div className="flex items-center justify-start space-x-2 py-4">
                <SheetDemo
                    openStatus={false}
                    loadingUser={false}
                    onOpenChange={setEditSheetOpen}
                    hiddenButton={Total === 0} titleButton={"New User"} title="Novo usuário">
                    <SimpleForm
                        title="Please, fill all inputs below"
                        fields={NewUserFields}
                        handleUser={handleTestNewUser}>
                    </SimpleForm>
                </SheetDemo>
                <SheetDemo
                    openStatus={editSheetOpen}
                    loadingUser={isPending}
                    onOpenChange={setEditSheetOpen}
                    handleOnClick={() => handleClickTransition(handleEditClick)}
                    hiddenButton={selectedUsers.size !== 1}
                    titleButton={"Edit User"}
                    title="Editando usuário"
                >
                    <SimpleForm
                        title="Please, fill all inputs below"
                        fields={EditUserFields}
                        handleUser={handleEditUser}
                    ></SimpleForm>
                </SheetDemo>

                <Button
                    hidden={selectedUsers.size === 0}
                    variant="outline"
                >
                    Delete
                </Button>
                <Button
                    hidden={selectedUsers.size === 0}
                    variant="outline"
                    onClick={() => { redirect(`${url_permissions}/${selectedUser?.ID}`) }}
                >
                    Edit User Permissions
                </Button>
            </div>
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead className="text-left">
                            <Checkbox
                                checked={selectedUsers.size === users.length}
                                onCheckedChange={HeaderCheckedHandle}
                            />
                        </TableHead>
                        {
                            headers.map((item, index) => (
                                <TableHead key={index}>{item}</TableHead>
                            ))
                        }
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {
                        users.map((user, index) => (
                            <TableRow
                                //className={"border-b transition-colors hover:bg-muted/50 has-aria-expanded:bg-muted/50 data-[state=selected]:bg-muted"}
                                key={index}>
                                <TableCell className="font-medium">
                                    <Checkbox
                                        checked={
                                            selectedUsers.has(user.ID)
                                        }
                                        onCheckedChange={
                                            (checked) => {
                                                toggleUser(user, checked === true)
                                            }
                                        }
                                        aria-label="Select all"
                                    />
                                </TableCell>
                                <TableCell className="font-medium">{user.ID}</TableCell>
                                <TableCell>{user.Name}</TableCell>
                                <TableCell>{user.DateCreation}</TableCell>
                                <TableCell>{user.UserType}</TableCell>
                            </TableRow>
                        ))
                    }
                </TableBody>
            </Table>
            <div className="flex items-center justify-between">
                <p className="text-gray-500 text-sm"><i>{selectedUsers.size} selected</i></p>
                <div className="flex items-center justify-end space-x-2 py-4">
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                            auth.setPage({ name: "management", Limit: Limit, Offset: Offset, Total: Total });
                            router.push(`${routes.management}?Limit=${Limit}&Offset=${Offset - Limit}`);
                        }}
                        disabled={previousButton}
                    >
                        Previous
                    </Button>
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                            auth.setPage({ name: "management", Limit: Limit, Offset: Offset, Total: Total });
                            router.push(`${routes.management}?Limit=${Limit}&Offset=${Offset + Limit}`);
                        }}
                        disabled={nextButton}
                    >
                        Next
                    </Button>
                </div>
            </div>
        </div>
    )
}
