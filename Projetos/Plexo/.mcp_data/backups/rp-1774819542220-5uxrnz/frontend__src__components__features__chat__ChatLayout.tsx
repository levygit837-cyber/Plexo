// ChatLayout - Main container based on Pencil Frame Base design (Plexo Chat Components)
import { ChatHeader } from './ChatHeader';
import { ChatSidebar } from './ChatSidebar';
import { ChatMessages } from './ChatMessages';
import { ChatSamples } from './ChatSamples';
import { ChatInputBar } from './ChatInputBar';

export const ChatLayout = () => {
    return (
        <div className="flex flex-col h-screen bg-gray-950 p-6">
            {/* Main Chat Container - equivalent to "Plexo Chat Components" frame */}
            <div className="flex flex-col flex-1 max-w-[1472px] mx-auto w-full bg-gray-950 rounded-3xl p-6 gap-6">
                {/* Header Zone */}
                <ChatHeader />

                {/* Body Row */}
                <div className="flex flex-1 gap-6">
                    {/* Sidebar Zone */}
                    <ChatSidebar />

                    {/* Messages Zone */}
                    <ChatMessages />

                    {/* Samples Zone */}
                    <ChatSamples />
                </div>

                {/* Input Bar Zone */}
                <ChatInputBar />
            </div>
        </div>
    );
};