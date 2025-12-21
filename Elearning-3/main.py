from event_loop_demo import run_event_loop
from threading_demo import run_threading
from callback_demo import run_callback
from future_promise_demo import run_future
from async_await_demo import run_async_await

def main():
    n = 5

    print("===== ASYNCHRONOUS SIMULATOR =====")
    print("1. Event-driven / Event Loop")
    print("2. Multithreading")
    print("3. Callback")
    print("4. Promise / Future")
    print("5. Async / Await")

    choice = int(input("Chon ki thuat: "))

    if choice == 1:
        run_event_loop(n)
    elif choice == 2:
        run_threading(n)
    elif choice == 3:
        run_callback(n)
    elif choice == 4:
        run_future(n)
    elif choice == 5:
        run_async_await(n)
    else:
        print("Lua chon khong hop le!")

if __name__ == "__main__":
    main()
