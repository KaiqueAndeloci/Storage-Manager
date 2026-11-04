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
import { InputPassword } from "@/components/custom/input/password"
import { fieldModel } from "@/Interfaces"


export function SimpleForm2(
    {
        fields, title, handleUser
    }: {
        fields: fieldModel[], title: string | undefined, handleUser: () => void
    }
) {

    return (
        <form onSubmit={() => { }} className="grid flex-1 auto-rows-min gap-6 px-4">
            <p hidden={!!title}>{title}</p>
            {
                fields.map(
                    (item, index) => (
                        <div key={index}>
                            {
                                (() => {
                                    switch (item.type) {
                                        case "text":
                                            return (
                                                <div className="grid gap-3" hidden={item.hidden}>
                                                    <Input
                                                        className={item.className}
                                                        maxLength={item.maxLength}
                                                        name={item.name} type="text"
                                                        placeholder={item.placeholder}
                                                        defaultValue={item.defaultValue}
                                                    />
                                                </div>
                                            );
                                        case "password":
                                            return (
                                                <InputPassword classNameDiv="grid gap-3" classNameInput={item.className} />
                                            );
                                        case "radio":
                                            return (
                                                <RadioButton
                                                    name={item.name}
                                                    label={item.label ? item.label : []}
                                                    getChecked={item.setRadioState}
                                                    optionChecked={item.radioState}
                                                ></RadioButton>
                                            );
                                        case "email":
                                            return (
                                                <div className="grid gap-3" hidden={item.hidden}>
                                                    <Input
                                                        className={item.className}
                                                        maxLength={item.maxLength}
                                                        name={item.name}
                                                        type="email"
                                                        placeholder={item.placeholder}
                                                        defaultValue={item.defaultValue}
                                                    />
                                                </div>
                                            )
                                        default:
                                            return (
                                                <div className="grid gap-3" hidden={item.hidden}>
                                                    <Input
                                                        className={item.className}
                                                        maxLength={item.maxLength}
                                                        name={item.name}
                                                        type={item.type}
                                                        placeholder={item.placeholder}
                                                        defaultValue={item.defaultValue}
                                                    />
                                                </div>
                                            );
                                    }
                                })()
                            }
                        </div>
                    )
                )
            }

            <ButtonSubmit />
        </form>
    )
}



