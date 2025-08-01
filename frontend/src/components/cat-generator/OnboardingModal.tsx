import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import catPng from "../../assets/cat.png";

export default function OnboardingModal({
  isOpen,
  onClose,
}: {
  isOpen: boolean;
  onClose: () => void;
}) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <div className="h-[20px] w-[20px]">
              <img src={catPng} alt="Cat" />
            </div>
            What is this?
          </DialogTitle>
        </DialogHeader>
        <DialogDescription>
          <p>
            This app shows how AI can <i>self-reflect and improve</i> through a
            feedback loop.
          </p>
          <ol className="mt-2 space-y-1">
            <li>
              1. A random cat image is used to generate a cartoon-style prompt.
            </li>
            <li>2. An image is created from that prompt using an AI model.</li>
            <li>
              3. A second AI model critiques the result and suggests
              improvements.
            </li>
            <li>4. The prompt is revised and the process repeats!</li>
          </ol>
        </DialogDescription>
      </DialogContent>
    </Dialog>
  );
}
