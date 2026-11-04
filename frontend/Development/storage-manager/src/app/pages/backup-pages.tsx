'use server'
import { routes } from "@/app/routes";


type Item = {
    title: string
    url: string
    description: string
}
export default async function Pages() {
    // const list_pages: Item[] = []
    const list_pages: Item[] = Object.entries(routes).map(
        ([key, value]) => ({
            title: key,
            url: value,
            description: '',
        })
    );
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