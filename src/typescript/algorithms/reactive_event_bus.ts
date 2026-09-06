/**
 * Reactive Event Bus with Backpressure and Type Safety
 */

export type EventHandler<T> = (event: T) => Promise<void> | void;

export interface EventSubscription {
  unsubscribe: () => void;
}

export class ReactiveEventBus {
  private handlers: Map<string, Set<EventHandler<any>>> = new Map();
  private maxListenersPerEvent: number;

  constructor(maxListenersPerEvent = 50) {
    this.maxListenersPerEvent = maxListenersPerEvent;
  }

  public subscribe<T>(eventType: string, handler: EventHandler<T>): EventSubscription {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, new Set());
    }

    const set = this.handlers.get(eventType)!;
    if (set.size >= this.maxListenersPerEvent) {
      console.warn(`[ReactiveEventBus] Max listeners (${this.maxListenersPerEvent}) exceeded for ${eventType}`);
    }

    set.add(handler);

    return {
      unsubscribe: () => {
        set.delete(handler);
        if (set.size === 0) {
          this.handlers.delete(eventType);
        }
      },
    };
  }

  public async publish<T>(eventType: string, payload: T): Promise<void> {
    const set = this.handlers.get(eventType);
    if (!set || set.size === 0) return;

    const promises: Promise<void>[] = [];
    for (const handler of set) {
      try {
        const result = handler(payload);
        if (result instanceof Promise) {
          promises.push(result);
        }
      } catch (err) {
        console.error(`[ReactiveEventBus] Error handling ${eventType}:`, err);
      }
    }

    if (promises.length > 0) {
      await Promise.all(promises);
    }
  }

  public clear(): void {
    this.handlers.clear();
  }
}
