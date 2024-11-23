"use client";

// import { useState } from "react";
import { Input } from "@/components/ui/input";
// import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
// import { SearchableDropdown } from "@/custom-components/SearchableDropdown";

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

import axios from "axios";

function SearchableDropdown({ optionsList = [], onSelect }) {
	const [open, setOpen] = useState(false);
	const [value, setValue] = useState("");
	const [options, setOptions] = useState([]);

	useEffect(() => {
		if (Array.isArray(optionsList)) {
			setOptions(optionsList);
		}
	}, [optionsList]);

	useEffect(() => {
		console.log("selected value: ", value);
	}, [value]);

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
						? options.find((option) => option.id === value)?.name
						: "Select option..."}
					<ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
				</Button>
			</PopoverTrigger>
			<PopoverContent className="w-[200px] p-0">
				<Command>
					<CommandInput placeholder="Search option..." />
					<CommandEmpty>No option found.</CommandEmpty>
					<CommandGroup>
						{options.map((option) => (
							<CommandItem
								key={option.id}
								value={option.name}
								onSelect={(currentValue) => {
									setValue(currentValue === value ? "" : option.id);
									setOpen(false);
									onSelect(currentValue === value ? "" : option.id);
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
						))}
					</CommandGroup>
				</Command>
			</PopoverContent>
		</Popover>
	);
}

// Your existing ChatUI component code here...

export default function ChatUI() {
	const [messages, setMessages] = useState([]);
	const [inputMessage, setInputMessage] = useState("");
	const [optionsList, setOptionsList] = useState([]);
	const [selectedPerson, setSelectedPerson] = useState(null);

	const handlePersonSelect = (id) => {
		setSelectedPerson(id);
	};

	// useEffect(() => {
	// 	const fetchOptions = async () => {
	// 	  try {
	// 		const response = await fetch('/api/options');
	// 		const data = await response.json();
	// 		setOptionsList(data);
	// 	  } catch (error) {
	// 		console.error('Error fetching options:', error);
	// 	  }
	// 	};

	// 	fetchOptions();
	//   }, [])

	useEffect(() => {
		const fetchOptions = async () => {
			try {
				const response = await axios.get("http://localhost:8080/profiles");
				console.log(response.data);
				setOptionsList(response.data);
			} catch (error) {
				console.error("Error fetching options:", error);
			}
		};

		fetchOptions();
	}, []);

	const sendMessage = () => {
		if (inputMessage.trim() !== "" && selectedPerson) {
			setMessages([...messages, { text: inputMessage, sender: "person" }]);

			console.log("Sending message:", inputMessage);

			// Send the message to the server
			axios
				.post(`http://localhost:8080/suggest-messages/${selectedPerson}`, {
					text: inputMessage,
				})
				.then((response) => {
					console.log("Message sent successfully:");
					console.log(response.data);

					setMessages([
						...messages,
						{ text: inputMessage, sender: "person" },
						{ text: response.data, sender: "user" },
					]);
				})
				.catch((error) => {
					console.error("Error sending message:", error);
				});

			setInputMessage("");
		}
	};

	return (
		<div className="flex flex-col h-screen">
			<div className="flex items-center justify-center h-screen">
				<img src="logo.png" alt="Logo" className="w-[632px] h-[355px]" />
			</div>
			<div className="ml-30 mr-30">
				<SearchableDropdown
					optionsList={optionsList}
					onSelect={handlePersonSelect}
				/>
			</div>
			<ScrollArea className="flex-grow p-4 min-h-[300px]">
				{messages.map((message, index) => (
					<div
						key={index}
						className={`flex ${
							message.sender === "user" ? "justify-end" : "justify-start"
						} mb-4`}
					>
						<div
							className={`flex items-center ${
								message.sender === "user" ? "flex-row-reverse" : "flex-row"
							}`}
						>
							<Avatar className="w-8 h-8" />
							<div
								className={`mx-2 p-2 rounded-lg ${
									message.sender === "user"
										? "bg-green-500 text-white"
										: "bg-gray-200"
								}`}
							>
								{message.text}
							</div>
						</div>
					</div>
				))}
			</ScrollArea>
			<div className="p-4 border-t">
				<div className="flex">
					<Input
						value={inputMessage}
						onChange={(e) => setInputMessage(e.target.value)}
						placeholder="Type a message..."
						className="flex-grow mr-2"
					/>
					<Button onClick={sendMessage}>Send</Button>
				</div>
			</div>
		</div>
	);
}

// function SearchableDropdown() {
// 	const [open, setOpen] = useState(false);
// 	const [value, setValue] = useState("");
// 	const [options, setOptions] = useState([]);
// 	const [loading, setLoading] = useState(false);

// 	useEffect(() => {
// 		if (Array.isArray(optionsList)) {
// 			setOptions(optionsList);
// 		}
// 	}, [optionsList]);

// 	useEffect(() => {
// 		console.log(options);
// 	}, [options]);

// 	return (
// 		<Popover open={open} onOpenChange={setOpen}>
// 			<PopoverTrigger asChild>
// 				<Button
// 					variant="outline"
// 					role="combobox"
// 					aria-expanded={open}
// 					className="w-[200px] justify-between"
// 				>
// 					{value
// 						? options.find((option) => option.id === value)?.label
// 						: "Select option..."}
// 					<ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
// 				</Button>
// 			</PopoverTrigger>
// 			<PopoverContent className="w-[200px] p-0">
// 				<Command>
// 					<CommandInput placeholder="Search option..." />
// 					<CommandEmpty>No option found.</CommandEmpty>
// 					<CommandGroup>
// 						{loading ? (
// 							<CommandItem>Loading...</CommandItem>
// 						) : (
// 							options.map((option) => (
// 								<CommandItem
// 									key={option.id}
// 									value={option.name}
// 									onSelect={(currentValue) => {
// 										setValue(currentValue === value ? "" : option.id);
// 										setOpen(false);
// 									}}
// 								>
// 									<Check
// 										className={cn(
// 											"mr-2 h-4 w-4",
// 											value === option.id ? "opacity-100" : "opacity-0"
// 										)}
// 									/>
// 									{option.name}
// 								</CommandItem>
// 							))
// 						)}
// 					</CommandGroup>
// 				</Command>
// 			</PopoverContent>
// 		</Popover>
// 	);
// }
