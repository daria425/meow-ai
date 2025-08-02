import { Dialog, DialogContent } from "@/components/ui/dialog";

export default function ThoughtBubble({
  thought,
  isOpen,
}: {
  thought: string;
  isOpen: boolean;
}) {
  return (
    <Dialog open={isOpen}>
      <DialogContent
        className="max-w-xs p-4 border-none shadow-lg [&>button]:hidden"
        style={{
          animation: "bounce 4s ease-in-out infinite",
        }}
      >
        <div className="mb-2 text-center">
          <p className="font-medium text-gray-900">
            ⋆⭒˚.⋆ AI had a thought! ⋆⭒˚.⋆
          </p>
        </div>
        <p className="text-xs text-gray-800">"{thought}"</p>
      </DialogContent>
    </Dialog>
  );
}
