'use server'
// import { LoginForm } from "@/components/custom/forms/login"
import { Suspense } from "react";
// import { Suspense, use, useState } from "react";
import Loading from '@/app/loading'
import { getUsersAction } from '@/requests/API_backend/index'
import { TableActions } from '@/components/custom/tables/managememt/index'
// import { useSearchParams } from 'next/navigation'
import { Users_table } from "@/Interfaces/index"


interface PageProps {
    searchParams: Promise<{
        Limit?: string;
        Offset?: string;
    }>;
}


export default async function Management({
    searchParams,
}: PageProps) {
    // const [Limit, setLimit] = useState(100);
    // const [Offset, setOffset] = useState(0);
    const params = await searchParams;


    const Limit = Number(params.Limit || 1);
    const Offset = Number(params.Offset || 0);
    // const Limit = Number(params.get('Limit')) || 100
    // const Offset = Number(params.get('Offset')) || 0

    let response = await getUsersAction({ Limit: Limit, Offset: Offset })
    let users: Users_table[] = []
    let total = 0;
    console.log(response)
    if (response.success === true) {
        for (let index = 0; index < response.response_api.Users.length; index++) {
            users.push(
                {
                    checked: false,
                    ID: index,
                    Name: response.response_api.Users[index].Name,
                    DateCreation: response.response_api.Users[index].DateCreation,
                    UserType: response.response_api.Users[index].UserType
                }
            )
        }
        if (response.response_api.Total !== undefined && response.response_api.Total !== null) {
            total = response.response_api.Total
        }
    }

    const headers = ["ID", "Nome", "Data de Criação", "Tipo de Usuário"]

    return (
        <Suspense fallback={<Loading></Loading>}>
            <TableActions Limit={Limit} Offset={Offset} Total={total} headers={headers} users={users}></TableActions>
        </Suspense>
    )
}