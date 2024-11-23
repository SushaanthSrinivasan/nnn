"use client";

import { useState, useEffect } from "react";
import { Check, ChevronsUpDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
	Command,
	CommandEmpty,
	CommandGroup,
	CommandInput,
	CommandItem,
} from "@/components/ui/command";
import {
	Popover,
	PopoverContent,
	PopoverTrigger,
} from "@/components/ui/popover";

export function SearchableDropdown({ optionsList = [] }) {
	const [open, setOpen] = useState(false);
	const [value, setValue] = useState("");
	const [options, setOptions] = useState([]);
	const [loading, setLoading] = useState(false);

	// useEffect(() => {
	// 	// const fetchOptions = async () => {
	// 	// 	setLoading(true);
	// 	// 	try {
	// 	// 		const response = await fetch("https://api.example.com/options");
	// 	// 		const data = await response.json();
	// 	// 		setOptions(data);
	// 	// 	} catch (error) {
	// 	// 		console.error("Error fetching options:", error);
	// 	// 	} finally {
	// 	// 		setLoading(false);
	// 	// 	}
	// 	// };

	// 	// fetchOptions();

	// 	setOptions(optionsList);
	// 	// console.log(options);
	// }, [optionsList]);

	useEffect(() => {
		if (Array.isArray(optionsList)) {
			setOptions(optionsList);
		}
	}, [optionsList]);

	useEffect(() => {
		console.log(options);
	}, [options]);

	return (
		<Popover open={open} onOpenChange={setOpen}>
			<PopoverTrigger asChild>
				<Button
					variant="outline"
					role="combobox"
					aria-expanded={open}
					className="w-[200px] justify-between"
				>
					{value
						? options.find((option) => option.id === value)?.label
						: "Select option..."}
					<ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
				</Button>
			</PopoverTrigger>
			<PopoverContent className="w-[200px] p-0">
				<Command>
					<CommandInput placeholder="Search option..." />
					<CommandEmpty>No option found.</CommandEmpty>
					<CommandGroup>
						{loading ? (
							<CommandItem>Loading...</CommandItem>
						) : (
							options.map((option) => (
								<CommandItem
									key={option.id}
									value={option.name}
									onSelect={(currentValue) => {
										setValue(currentValue === value ? "" : option.id);
										setOpen(false);
									}}
								>
									<Check
										className={cn(
											"mr-2 h-4 w-4",
											value === option.id ? "opacity-100" : "opacity-0"
										)}
									/>
									{option.name}
								</CommandItem>
							))
						)}
					</CommandGroup>
				</Command>
			</PopoverContent>
		</Popover>
	);
}

export default SearchableDropdown;
