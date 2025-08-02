import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogClose,
  DialogFooter,
} from "@/components/ui/dialog";
import catPng from "../../assets/cat.png";
import { Button } from "../ui/button";
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
            <div className="h-[30px] w-[30px]">
              <img src={catPng} alt="Cat" />
            </div>
            <h2>What is this?</h2>
          </DialogTitle>
        </DialogHeader>
        <DialogDescription>
          <h5>
            This app shows how AI can <i>self-reflect and improve</i> through a
            feedback loop.
          </h5>
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
          <h5 className="mt-2">
            You'll see each step of the process in real time:
          </h5>
          <ul className="mt-2 space-y-1">
            <li>- The prompt used</li>
            <li>- The generated image</li>
            <li>- The AI's critique</li>
          </ul>
        </DialogDescription>
        <DialogFooter>
          <DialogClose asChild>
            <Button className="bg-gradient-to-r from-[#f5a327] to-[#c157c7] text-white text-xs">
              Start Generating
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
