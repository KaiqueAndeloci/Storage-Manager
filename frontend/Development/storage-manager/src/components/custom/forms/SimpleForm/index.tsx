"use client"
import { ButtonSubmit } from "@/components/custom/button";
import { fieldModel } from "@/Interfaces"
import { SubmitEventHandler, SubmitEvent } from "react";
import { RenderFields } from "@/components/custom/util/index"


export function SimpleForm(
    {
        fields, title, handleUser, handleOnClick
    }: {
        fields: fieldModel[],
        title: string | undefined,
        handleUser: (e: SubmitEvent<HTMLFormElement>) => void,
        handleOnClick?: () => void
    }
) {

    return (
        <form onSubmit={(e) => { e.preventDefault(); handleUser(e) }} className="grid flex-1 auto-rows-min gap-6 px-4">
            <p hidden={!!title}>{title}</p>
            {
                RenderFields({ fields })
            }

            <ButtonSubmit handleOnClick={handleOnClick} />
        </form>
    )
}



