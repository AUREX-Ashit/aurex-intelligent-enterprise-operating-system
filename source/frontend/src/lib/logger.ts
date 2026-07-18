/**
 * Logging abstraction.
 *
 * Nothing in the application should call `console.*` directly — every call
 * site imports `logger` instead. That gives the platform exactly one place
 * to change later (structured JSON output, a remote log sink, per-level
 * filtering by environment) without touching every component that logs
 * something.
 *
 * Deliberately never accepts a bare Error/object for the message itself —
 * callers pass a plain description plus a `context` record, so any future
 * remote sink is never handed something that might unexpectedly contain
 * sensitive data attached to an exception's own properties.
 */

type LogContext = Record<string, unknown>;

type LogLevel = "debug" | "info" | "warn" | "error";

function emit(level: LogLevel, message: string, context?: LogContext): void {
  const entry = {
    level,
    message,
    ...(context ? { context } : {}),
    timestamp: new Date().toISOString(),
  };

  // This is the one sanctioned call site for console.* in the application;
  // no-console isn't an active rule in this project's ESLint config, so no
  // suppression directive is needed here.
  console[level === "debug" ? "debug" : level](entry);
}

export const logger = {
  debug(message: string, context?: LogContext): void {
    if (process.env.NODE_ENV !== "production") {
      emit("debug", message, context);
    }
  },
  info(message: string, context?: LogContext): void {
    emit("info", message, context);
  },
  warn(message: string, context?: LogContext): void {
    emit("warn", message, context);
  },
  error(message: string, context?: LogContext): void {
    emit("error", message, context);
  },
};
