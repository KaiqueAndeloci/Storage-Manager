'use server'
import { ButtonSubmit } from "@/components/custom/button";
// import { useSearchParams } from 'next/navigation'
import routes from '@/app/routes'
// import { redirect } from 'next/navigation'
// import Link from "next/link"


export default async function Home() {
    // function navigateDashboard() {
    //     const params = useSearchParams()
    //     const from = params.get('redirect') || routes.dashboard
    //     redirect(from)
    // }
    //scroll-m-20 text-center text-4xl font-extrabold tracking-tight text-balance
    return (
        <div className="text-white flex flex-col justify-center items-center gap-6 min-w-sm mx-6 sm:mx-16 md:mx-24 lg:mx-auto lg:w-auto">
            <div className="mt-10 flex flex-col justify-center items-center gap-6 text-center scroll-m-20 font-extrabold tracking-tight text-balance">
                <h1 className="text-4xl md:text-7xl w-fit">The everything app, for storage manager</h1>
                <p className="font-bold w-fit text-gray-300">One app for professional projects, organization, maximum time-efficiency and more.</p>
                {/* <Link href={routes.login}><ButtonSubmit size={null} className="h-15 text-lg rounded-md px-16" text="Get started" /></Link> */}
                <a href={routes.login}><ButtonSubmit size={null} className="h-15 text-lg rounded-md px-16 hover:cursor-pointer" text="Get started" /></a>
            </div>
            <br />
            <h2 className="text-2xl font-bold">Maximize your work efficiency</h2>
            <div className="w-fit px-20 py-10 mx-20 flex flex-col justify-center items-center gap-6 border-white border-2 rounded-md">
                <h3>Organization</h3>
                <p>Navigation seppared by cards</p>
                <p>Differing views of your containers</p>
            </div>
            <div className="w-fit px-20 py-10 mx-20 flex flex-col justify-center items-center gap-6 border-white border-2 rounded-md">
                <h3>Dashboard</h3>
                <p>Clear top view of your products</p>
            </div>
            <div className="w-fit px-20 py-10 mx-20 flex flex-col justify-center items-center gap-6 border-white border-2 rounded-md">
                <h3>Management</h3>
                <p>Clear management of your products</p>
            </div>
        </div>
    )
}