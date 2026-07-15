'use client'
import { MoreHorizontalIcon } from "lucide-react"
import { redirect, useRouter } from 'next/navigation'
import { useSearchParams } from 'next/navigation'
import { Button } from "@/components/ui/button"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
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
import { Users_table } from "@/Interfaces/index"
import { useAuth } from '@/Providers/index'
import routes from '@/app/routes'

export function TableActions({ users, headers, Total, Limit, Offset }: { users: Users_table[], headers: string[], Total: number, Limit: number, Offset: number }) {
    const auth = useAuth()
    const router = useRouter()
    const [LimitState, setLimit] = useState(Limit);
    const [OffsetState, setOffset] = useState(Offset);
    const [PageNumber, setPageNumber] = useState(1);
    const [usersList, setUsersList] = useState(users);
    const [allchecked, setAllchecked] = useState(false);
    const [selected, setSelected] = useState<number[]>([]);
    const previousButton = 0 < Offset ? false : true
    const nextButton = Limit + Offset < Total ? false : true
    const params = useSearchParams()
    const LimitParam = params.get('Limit') || Limit
    const OffsetParam = params.get('Offset') || Offset
    function NextPage({ page }: { page: number }) {
        setLimit(Limit * (page + PageNumber));
        setPageNumber(page + PageNumber);
    };
    const hasSelected = usersList.some(user => user.checked);
    const selectedCount = usersList.filter(user => user.checked).length;
    function HeaderCheckedHandle(checked: boolean | 'indeterminate') {
        setSelected(users.map((user, index) => user.checked ? index : null).filter(index => index !== null));
        console.log(selected)

        setAllchecked(usersList.every(user => user.checked) === true);

        setUsersList(current =>
            current.map(user => ({
                ...user,
                checked: checked === true
            }))
        );
        return
    }

    return (
        <div className="bg-white p-5 border-2 border-b-gray-50 rounded-md">
            <div className="flex items-center justify-start space-x-2 py-4">
                <Button
                    variant="outline"
                    hidden={Total === 0}
                >
                    New
                </Button>
                <Button
                    hidden={selectedCount !== 1}
                    variant="outline"
                >
                    Edit
                </Button>

                <Button
                    hidden={selectedCount === 0}
                    variant="outline"
                >
                    Delete
                </Button>
            </div>
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead className="text-left">
                            <Checkbox
                                checked={usersList.every(user => user.checked) === true}
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
                        usersList.map((user, index) => (
                            <TableRow
                                //className={"border-b transition-colors hover:bg-muted/50 has-aria-expanded:bg-muted/50 data-[state=selected]:bg-muted"}
                                key={index}>
                                <TableCell className="font-medium">
                                    <Checkbox
                                        checked={
                                            usersList[index].checked
                                        }
                                        onCheckedChange={
                                            (checked) => {
                                                setSelected(users.map((user, index) => user.checked ? index : null).filter(index => index !== null));

                                                setUsersList(current =>
                                                    current.map((item, i) =>
                                                        i === index
                                                            ? { ...item, checked: checked === true }
                                                            : item
                                                    )
                                                )
                                            }
                                        }
                                        aria-label="Select all"
                                    />
                                </TableCell>
                                <TableCell className="font-medium">{index}</TableCell>
                                <TableCell>{user.Name}</TableCell>
                                <TableCell>{user.DateCreation}</TableCell>
                                <TableCell>{user.UserType}</TableCell>
                            </TableRow>
                        ))
                    }
                </TableBody>
            </Table>
            <div className="flex items-center justify-end space-x-2 py-4">
                <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                        auth.setPage({ name: "management", Limit: Limit, Offset: Offset, Total: Total });
                        //redirect(`${routes.management}?Limit=${Limit}&Offset=${Offset - Limit}`, 'push');
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
                        //redirect(`${routes.management}?Limit=${Limit}&Offset=${Offset + Limit}`, 'push');
                    }}
                    disabled={nextButton}
                >
                    Next
                </Button>
            </div>
        </div>
    )
}
