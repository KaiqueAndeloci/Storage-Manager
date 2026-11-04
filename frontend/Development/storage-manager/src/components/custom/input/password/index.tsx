"use client"
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from '@/components/ui/label';
import { useState } from "react";

export function InputPassword(
    {
        classNameDiv, classNameInput
    }: {
        classNameDiv: string, classNameInput: string
    }
) {
    const [show, setShow] = useState(false);

    return (
        <div className={classNameDiv}>
            <Input className={classNameInput} maxLength={100} name={'password'} type={show ? 'text' : 'password'} placeholder="Password" />
            <div className="w-full flex gap-4">
                <Checkbox onCheckedChange={() => { setShow(!show) }} id="pass"></Checkbox>
                <Label htmlFor="pass" className={classNameInput}>Show password</Label>
            </div>
        </div>
    )
}