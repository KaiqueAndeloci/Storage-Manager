'use server'
import routes from "@/app/routes";


type Item = {
    title: string
    url: string
    description: string
}
export default async function Storages() {
    // const list_pages: Item[] = []
    const list_pages: Item[] = [
        {
            title: "Storage 1",
            url: "/pages/storages/storage1",
            description: ''
        },
        {
            title: "Storage 2",
            url: "/pages/storages/storages2",
            description: ''
        }
    ]
    return (
        <div className="w-full">
            <ul>
                {
                    list_pages.map((item) => (
                        <li key={item.title} className="h-20 w-full border-2 border-b rounded-md">
                            <a className="w-full h-full justify-center items-center flex" href={item.url}>
                                <p className="w-fit h-fit">{item.title}</p>
                            </a>
                        </li>
                    ))
                }
            </ul>
        </div>
    )
}