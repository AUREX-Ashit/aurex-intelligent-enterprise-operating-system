import { useEffect, useRef, type RefObject } from "react";

const FOCUSABLE_SELECTOR =
  'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';

interface UseOverlayOptions {
  /** Whether the overlay is currently open/visible. */
  open: boolean;
  onClose: () => void;
  /** Outside-click boundary. Modal/Drawer close via their own backdrop instead, so pass `closeOnOutsideClick: false` (the default) for those. */
  containerRef: RefObject<HTMLElement | null>;
  /** Focus-trap boundary, if narrower than `containerRef` (e.g. Menu traps focus to its panel, not its trigger). Defaults to `containerRef`. */
  trapRef?: RefObject<HTMLElement | null>;
  closeOnOutsideClick?: boolean;
}

/**
 * Shared overlay behaviour for every dismissible panel (Modal, Drawer,
 * Menu, Notification Center): Escape-to-close, Tab/Shift+Tab focus
 * trapping within the panel, initial focus moved into the panel on open,
 * and focus restored to whatever triggered it on close. Each of these
 * components previously hand-rolled its own Escape/outside-click effect
 * with no focus trap or restoration at all — consolidating here means
 * every current and future overlay gets standards-compliant dialog/menu
 * keyboard behaviour for free rather than re-deriving it per component.
 */
export function useOverlay({
  open,
  onClose,
  containerRef,
  trapRef,
  closeOnOutsideClick = false,
}: UseOverlayOptions) {
  const previouslyFocused = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!open) return;

    const trapElement = (trapRef ?? containerRef).current;
    previouslyFocused.current = document.activeElement as HTMLElement | null;

    const focusable = trapElement
      ? Array.from(trapElement.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR))
      : [];
    (focusable[0] ?? trapElement)?.focus();

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        onClose();
        return;
      }

      if (event.key !== "Tab" || !trapElement) return;

      const elements = Array.from(trapElement.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR));
      if (elements.length === 0) {
        event.preventDefault();
        return;
      }

      const first = elements[0];
      const last = elements[elements.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }

    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        onClose();
      }
    }

    document.addEventListener("keydown", handleKeyDown);
    if (closeOnOutsideClick) document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      if (closeOnOutsideClick) document.removeEventListener("mousedown", handleClickOutside);
      previouslyFocused.current?.focus();
    };
  }, [open, onClose, containerRef, trapRef, closeOnOutsideClick]);
}
