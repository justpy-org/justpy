import justpy as jp

ui_string = '''
<div id="app" class="h-screen flex flex-col">
  <header class="flex flex-shrink-0">
    <div class="flex-shrink-0 px-4 py-3 bg-gray-700 lg:w-64 lg:bg-gray-800">
      <button
        @click="sidebarOpen = true"
        class="block text-gray-400 hover:text-gray-200 sm:hidden"
      >
        <svg class="h-6 w-6" viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M3 6a1 1 0 011-1h16a1 1 0 110 2H4a1 1 0 01-1-1zM3 12a1 1 0 011-1h16a1 1 0 110 2H4a1 1 0 01-1-1zM4 17a1 1 0 100 2h7a1 1 0 100-2H4z"
          />
        </svg>
      </button>

      <button class="hidden sm:flex sm:items-center sm:w-full">
        <img
          class="h-8 w-8 rounded-full object-cover"
          src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=144&h=144&q=80"
          alt=""
        />
        <span
          class="hidden lg:inline ml-4 mr-2 text-sm font-medium text-white"
        >
          Monica White
        </span>
        <svg
          class="ml-2 h-6 w-6 fill-current text-gray-400 lg:ml-auto"
          viewBox="0 0 24 24"
        >
          <path
            d="M7.293 9.293a1 1 0 011.414 0L12 12.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
          />
        </svg>
      </button>
    </div>
    <div
      class="flex-1 flex items-center justify-between pl-2 pr-6 bg-gray-700 lg:px-6"
    >
      <nav class="hidden sm:flex">
        <a
          href="#"
          class="inline-block px-3 py-2 bg-gray-800 rounded-lg leading-none text-sm font-medium text-white"
        >
          Mailbox
        </a>
        <a
          href="#"
          class="ml-2 inline-block px-3 py-2 rounded-lg leading-none text-sm font-medium text-white hover:bg-gray-600"
        >
          Customers
        </a>
        <a
          href="#"
          class="ml-2 inline-block px-3 py-2 rounded-lg leading-none text-sm font-medium text-white hover:bg-gray-600"
        >
          Reporting
        </a>
        <a
          href="#"
          class="ml-2 inline-block px-3 py-2 rounded-lg leading-none text-sm font-medium text-white hover:bg-gray-600"
        >
          Manage
        </a>
      </nav>
      <div class="ml-auto flex items-center">
        <button class="lg:hidden ml-5 text-gray-400 hover:text-gray-200">
          <svg class="h-5 w-5 fill-current" viewBox="0 0 24 24">
            <path
              d="M10 4a6 6 0 100 12 6 6 0 000-12zm-8 6a8 8 0 1114.32 4.906l5.387 5.387a1 1 0 01-1.414 1.414l-5.387-5.387A8 8 0 012 10z"
            />
          </svg>
        </button>
        <div class="hidden lg:block relative w-64">
          <span class="absolute inset-y-0 left-0 flex items-center pl-2">
            <svg
              class="h-5 w-5 fill-current text-gray-500"
              viewBox="0 0 24 24"
            >
              <path
                d="M10 4a6 6 0 100 12 6 6 0 000-12zm-8 6a8 8 0 1114.32 4.906l5.387 5.387a1 1 0 01-1.414 1.414l-5.387-5.387A8 8 0 012 10z"
              />
            </svg>
          </span>
          <input
            class="block pl-9 pr-4 py-2 w-full bg-gray-800 rounded-lg text-sm placeholder-gray-400 text-white focus:bg-white focus:placeholder-gray-600 focus:text-gray-900 focus:outline-none"
            placeholder="Search"
          />
        </div>
        <button class="ml-5 text-gray-400 hover:text-gray-200">
          <svg class="h-5 w-5 fill-current" viewBox="0 0 24 24">
            <path
              d="M9.018 4.665a3 3 0 015.964 0A7 7 0 0119 11v3.159c0 .273.109.535.302.729l1.405 1.405A1 1 0 0120 18H4a1 1 0 01-.707-1.707l1.405-1.405c.193-.194.302-.456.302-.73V11a7 7 0 014.018-6.335zM12 4a1 1 0 00-1 1v1.049l-.667.235A5.002 5.002 0 007 11v3.159c0 .669-.221 1.315-.623 1.841h11.246A3.032 3.032 0 0117 14.159V11a5.002 5.002 0 00-3.333-4.716L13 6.05V5a1 1 0 00-1-1zM10 18a2 2 0 004 0h2a4 4 0 11-8 0h2z"
            />
          </svg>
        </button>
        <button class="ml-4 text-gray-400 hover:text-gray-200">
          <svg class="h-5 w-5 fill-current" viewBox="0 0 24 24">
            <path d="M12 18a1 1 0 100-2 1 1 0 000 2z" />
            <path
              d="M12 4a8 8 0 100 16 8 8 0 000-16zM2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12z"
            />
            <path
              d="M12 8c-1.472 0-2.528.706-2.868 1.426a1 1 0 01-1.809-.852C8.082 6.964 9.99 6 12 6c1.3 0 2.515.394 3.428 1.079C16.343 7.764 17 8.786 17 10c0 2.07-1.834 3.508-3.817 3.889a.31.31 0 00-.162.083A.107.107 0 0013 14a1 1 0 01-2 0c0-1.142.909-1.904 1.805-2.075C14.279 11.642 15 10.729 15 10c0-.443-.237-.92-.771-1.321C13.694 8.278 12.909 8 12 8z"
            />
          </svg>
        </button>
      </div>
    </div>
  </header>
  <div class="flex-1 flex overflow-hidden">
    <div
      
      class="z-30 fixed inset-y-0 left-0 w-64 bg-gray-100 border-r overflow-y-auto sm:static sm:block sm:translate-x-0 sm:transition-none"
    >
      <div class="absolute top-0 left-0 pl-4 pt-3 sm:hidden">
        <button
          @click="sidebarOpen = false"
          class="block text-gray-600 hover:text-gray-800"
        >
          <svg class="h-6 w-6" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M17.293 18.707a1 1 0 001.414-1.414L13.414 12l5.293-5.293a1 1 0 00-1.414-1.414L12 10.586 6.707 5.293a1 1 0 00-1.414 1.414L10.586 12l-5.293 5.293a1 1 0 101.414 1.414L12 13.414l5.293 5.293z"
            />
          </svg>
        </button>
      </div>
      <nav class="mt-16 sm:mt-0">
        <div class="px-6 sm:hidden">
          <a href="#" class="block py-1  text-sm font-medium text-gray-900">
            Mailbox
          </a>
          <a
            href="#"
            class="mt-2 block py-1  text-sm font-medium text-gray-900"
          >
            Customers
          </a>
          <a
            href="#"
            class="mt-2 block py-1  text-sm font-medium text-gray-900"
          >
            Reporting
          </a>
          <a
            href="#"
            class="mt-2 block py-1  text-sm font-medium text-gray-900"
          >
            Manage
          </a>
        </div>
        <div class="mt-8 px-6">
          <h2
            class="text-xs font-semibold text-gray-600 uppercase tracking-wide"
          >
            Mailboxes
          </h2>
          <div class="mt-3">
            <a
              href="#"
              class="-mx-3 px-3 py-2 flex items-center justify-between text-sm font-medium bg-gray-200 rounded-lg"
            >
              <span class="inline-flex">
                <svg
                  class="h-6 w-6 fill-current text-gray-700"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M3 6a3 3 0 013-3h12a3 3 0 013 3v12a3 3 0 01-3 3H6a3 3 0 01-3-3V6zm3-1a1 1 0 00-1 1v6h1.586A2 2 0 018 12.586L10.414 15h3.172L16 12.586A2 2 0 0117.414 12H19V6a1 1 0 00-1-1H6zm13 9h-1.586L15 16.414a2 2 0 01-1.414.586h-3.172A2 2 0 019 16.414L6.586 14H5v4a1 1 0 001 1h12a1 1 0 001-1v-4z"
                  />
                </svg>
                <span class="ml-2 text-gray-900">Inbox</span>
              </span>
              <span
                class="inline-block w-8 text-center py-1 leading-none text-xs font-semibold text-gray-700 bg-gray-300 rounded-full"
              >
                6
              </span>
            </a>
            <a
              href="#"
              class="mt-2 -mx-3 px-3 py-2 flex items-center justify-between text-sm font-medium hover:bg-gray-200 rounded-lg"
            >
              <span class="inline-flex">
                <svg
                  class="h-6 w-6 fill-current text-gray-500"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M5 4a1 1 0 00-1 1v9.17c.313-.11.65-.17 1-.17h6.5a1 1 0 01.707.293l.707.707h6.468l-2.276-4.553a1 1 0 010-.894L19.382 5H13v4a1 1 0 11-2 0V4H5zm7.914-1H21a1 1 0 01.894 1.447L19.118 10l2.776 5.553A1 1 0 0121 17h-8.5a1 1 0 01-.707-.293L11.086 16H5a1 1 0 00-1 1v4a1 1 0 11-2 0V5a3 3 0 013-3h6.5a1 1 0 01.707.293l.707.707z"
                  />
                </svg>
                <span class="ml-2 text-gray-700">Flagged</span>
              </span>
            </a>
            <a
              href="#"
              class="mt-2 -mx-3 px-3 py-2 flex items-center justify-between text-sm font-medium hover:bg-gray-200 rounded-lg"
            >
              <span class="inline-flex">
                <svg
                  class="h-6 w-6 fill-current text-gray-500"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M19.707 4.293a1 1 0 00-1.414 0L10 12.586V14h1.414l8.293-8.293a1 1 0 000-1.414zM16.88 2.879A3 3 0 1121.12 7.12l-8.585 8.586a1 1 0 01-.708.293H9a1 1 0 01-1-1v-2.828a1 1 0 01.293-.708l8.586-8.585zM6 6a1 1 0 00-1 1v11a1 1 0 001 1h11a1 1 0 001-1v-5a1 1 0 112 0v5a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h5a1 1 0 110 2H6z"
                  />
                </svg>
                <span class="ml-2 text-gray-700">Drafts</span>
              </span>
              <span
                class="inline-block w-8 text-center py-1 leading-none text-xs font-semibold text-gray-700 bg-gray-300 rounded-full"
              >
                2
              </span>
            </a>
            <a
              href="#"
              class="mt-2 -mx-3 px-3 py-2 flex items-center justify-between text-sm font-medium hover:bg-gray-200 rounded-lg"
            >
              <span class="inline-flex">
                <svg
                  class="h-6 w-6 fill-current text-gray-500"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M12 4a8 8 0 00-6.598 12.526A14.943 14.943 0 0112 15c2.366 0 4.606.548 6.598 1.526A8 8 0 0012 4zm5.199 14.08A12.954 12.954 0 0012 17c-1.85 0-3.607.386-5.199 1.08A7.968 7.968 0 0012 20c1.985 0 3.8-.723 5.199-1.92zM2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12zm10-4a2 2 0 100 4 2 2 0 000-4zm-4 2a4 4 0 118 0 4 4 0 01-8 0z"
                  />
                </svg>
                <span class="ml-2 text-gray-700">Assigned</span>
              </span>
              <span
                class="inline-block w-8 text-center py-1 leading-none text-xs font-semibold text-gray-700 bg-gray-300 rounded-full"
              >
                1
              </span>
            </a>
            <a
              href="#"
              class="mt-2 -mx-3 px-3 py-2 flex items-center justify-between text-sm font-medium hover:bg-gray-200 rounded-lg"
            >
              <span class="inline-flex">
                <svg
                  class="h-6 w-6 fill-current text-gray-500"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M12 4a8 8 0 100 16 8 8 0 000-16zM2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12zm13.707-2.707a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-2-2a1 1 0 111.414-1.414L11 12.586l3.293-3.293a1 1 0 011.414 0z"
                  />
                </svg>
                <span class="ml-2 text-gray-700">Closed</span>
              </span>
            </a>
            <a
              href="#"
              class="mt-2 -mx-3 px-3 py-2 flex items-center justify-between text-sm font-medium hover:bg-gray-200 rounded-lg"
            >
              <span class="inline-flex">
                <svg
                  class="h-6 w-6 fill-current text-gray-500"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M2 6a3 3 0 013-3h14a3 3 0 011 5.83V18a3 3 0 01-3 3H7a3 3 0 01-3-3V8.83A3.001 3.001 0 012 6zm4 3v9a1 1 0 001 1h10a1 1 0 001-1V9H6zM5 5a1 1 0 000 2h14a1 1 0 100-2H5zm4 7a1 1 0 011-1h4a1 1 0 110 2h-4a1 1 0 01-1-1z"
                  />
                </svg>
                <span class="ml-2 text-gray-700">Junk</span>
              </span>
            </a>
          </div>
          <h2
            class="mt-8 text-xs font-semibold text-gray-600 uppercase tracking-wide"
          >
            Folders
          </h2>
          <div class="mt-4">
            <a href="#" class="block text-sm font-medium text-gray-700">
              Refunds
            </a>
            <a href="#" class="mt-4 block text-sm font-medium text-gray-700">
              Discounts
            </a>
            <a href="#" class="mt-4 block text-sm font-medium text-gray-700">
              Bugs
            </a>
          </div>
        </div>
        <div class="mt-8 p-6 border-t sm:hidden">
          <div class="flex items-center">
            <img
              class="h-8 w-8 rounded-full object-cover"
              src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=144&h=144&q=80"
              alt=""
            />
            <span class="ml-4 mr-2 text-sm font-medium text-gray-800">
              Monica White
            </span>
          </div>
          <div class="mt-4">
            <a href="#" class="block text-sm font-medium text-gray-700">
              Settings
            </a>
            <a href="#" class="mt-4 block text-sm font-medium text-gray-700">
              Log out
            </a>
          </div>
        </div>
      </nav>
    </div>
    <main class="flex-1 flex bg-gray-200">
      <div
        class="hidden lg:flex flex-col relative z-10 w-full max-w-xs flex-grow flex-shrink-0 border-r bg-gray-300"
      >
        <div
          class="flex-shrink-0 px-4 py-2 flex items-center justify-between border-b bg-gray-200"
        >
          <button
            class="flex items-center text-xs font-semibold text-gray-600"
          >
            Sorted by Date
            <svg
              class="ml-1 h-6 w-6 fill-current text-gray-500"
              viewBox="0 0 24 24"
            >
              <path
                d="M7.293 9.293a1 1 0 011.414 0L12 12.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
              />
            </svg>
          </button>
          <button>
            <svg
              class="h-6 w-6 fill-current text-gray-500"
              viewBox="0 0 24 24"
            >
              <path
                d="M16 3H3a1 1 0 000 2h13a1 1 0 100-2zm-4 4H3a1 1 0 000 2h9a1 1 0 100-2zm-9 4h6a1 1 0 110 2H3a1 1 0 110-2zm9.293.293l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L18 10.414V20a1 1 0 11-2 0v-9.586l-2.293 2.293a1 1 0 01-1.414-1.414z"
              />
            </svg>
          </button>
        </div>
        <div class="flex-1 overflow-y-auto">
          <div class="shadow">
            <div>
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-indigo-100 border-l-4 border-indigo-500"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Joe Armstrong
                  </span>
                  <span class="text-sm text-gray-600">
                    1 day ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Re: Student Discount?
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Gloria Roberston
                  </span>
                  <span class="text-sm text-gray-600">
                    2 days ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Refund
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Pat Steward
                  </span>
                  <span class="text-sm text-gray-600">
                    4 days ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Issue with reporting
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Jerome Warren
                  </span>
                  <span class="text-sm text-gray-600">
                    4 days ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Email not working
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Gladys Mccoy
                  </span>
                  <span class="text-sm text-gray-600">
                    4 days ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Do you have a student discount?
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Jorge Murphy
                  </span>
                  <span class="text-sm text-gray-600">
                    1 week ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Not what I expected
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Paxton Walter
                  </span>
                  <span class="text-sm text-gray-600">
                    1 week ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  SEO opportunity
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Kristopher Donnelly
                  </span>
                  <span class="text-sm text-gray-600">
                    2 weeks ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Don't know where to start
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
          </div>
        </div>
      </div>
      <div class="flex-1 flex flex-col w-0 overflow-hidden">
        <div class="relative shadow-md">
          <div
            class="flex items-center justify-between px-5 py-4 bg-gray-100 border-b"
          >
            <div class="flex items-center">
              <button>
                <svg
                  class="h-6 w-6 fill-current text-gray-600"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M9.707 3.293a1 1 0 010 1.414L5.414 9H13a9 9 0 019 9v2a1 1 0 11-2 0v-2a7 7 0 00-7-7H5.414l4.293 4.293a1 1 0 01-1.414 1.414l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 0z"
                  />
                </svg>
              </button>
              <button class="ml-6">
                <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none">
                  <circle
                    class="fill-current text-gray-600"
                    cx="7"
                    cy="7"
                    r="1"
                  />
                  <path
                    class="stroke-current text-gray-600"
                    d="M12 3H7a4 4 0 00-4 4v5c0 .512.195 1.024.586 1.414l7 7a2 2 0 002.828 0l7-7a2 2 0 000-2.828l-7-7A1.993 1.993 0 0012 3z"
                    stroke-width="2"
                  />
                </svg>
              </button>
              <button class="ml-6">
                <svg
                  class="h-6 w-6 fill-current text-gray-600"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M12 4a8 8 0 00-6.598 12.526A14.943 14.943 0 0112 15c2.366 0 4.606.548 6.598 1.526A8 8 0 0012 4zm5.199 14.08A12.954 12.954 0 0012 17c-1.85 0-3.607.386-5.199 1.08A7.968 7.968 0 0012 20c1.985 0 3.8-.723 5.199-1.92zM2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12zm10-4a2 2 0 100 4 2 2 0 000-4zm-4 2a4 4 0 118 0 4 4 0 01-8 0z"
                  />
                </svg>
              </button>
              <button class="ml-6">
                <svg
                  class="h-6 w-6 fill-current text-gray-600"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M5 6a1 1 0 00-1 1v10a1 1 0 001 1h14a1 1 0 001-1V9a1 1 0 00-1-1h-6.414l-2-2H5zM2 7a3 3 0 013-3h6.414l2 2H19a3 3 0 013 3v8a3 3 0 01-3 3H5a3 3 0 01-3-3V7zm10 2a1 1 0 011 1v3.586l1.293-1.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 111.414-1.414L11 13.586V10a1 1 0 011-1z"
                  />
                </svg>
              </button>
              <button class="ml-6">
                <svg
                  class="h-6 w-6 fill-current text-gray-600"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M7 12a2 2 0 11-4 0 2 2 0 014 0zm7 0a2 2 0 11-4 0 2 2 0 014 0zm5 2a2 2 0 100-4 2 2 0 000 4z"
                  />
                </svg>
              </button>
            </div>
            <div class="flex items-center">
              <button>
                <svg
                  class="h-6 w-6 text-gray-600"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  fill="none"
                >
                  <path
                    d="M19 9l-7 7-7-7"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </button>
              <button class="ml-2">
                <svg
                  class="h-6 w-6 text-gray-600"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                >
                  <path
                    d="M5 16l7-7 7 7"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </button>
            </div>
          </div>
          <div class="flex items-center justify-between px-5 py-4 bg-white">
            <h3
              class="text-base lg:text-lg xl:text-xl text-gray-900 truncate"
            >
              Re: Student discount?
            </h3>
            <div class="ml-4 flex-shrink-0">
              <span class="text-sm lg:text-base">#1428</span>
              <span
                class="ml-2 text-xs font-semibold text-green-900 bg-green-200 rounded-full leading-none px-2 py-1 lg:text-sm"
                >Active</span
              >
            </div>
          </div>
        </div>
        <div class="p-3 flex-1 overflow-y-auto">
          <article
            class="px-6 pt-4 pb-6 xl:px-10 xl:pt-6 xl:pb-8 bg-white rounded-lg shadow"
          >
            <div class="flex items-center md:block">
              <div>
                <img
                  class="md:hidden h-9 w-8 rounded-full object-cover"
                  src="https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3.5&w=144&h=144&q=80"
                  alt=""
                />
              </div>
              <div
                class="ml-3 md:ml-0 md:flex md:items-center md:justify-between"
              >
                <p class="text-base font-semibold leading-tight xl:text-lg">
                  <span class="text-gray-900">Joe Armstrong</span>
                  <span class="text-gray-600">wrote</span>
                </p>
                <div class="flex items-center">
                  <span class="text-sm text-gray-600">
                    Yesterday at 7:24 AM
                  </span>
                  <img
                    class="hidden md:block ml-5 h-9 w-8 rounded-full object-cover"
                    src="https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3.5&w=144&h=144&q=80"
                    alt=""
                  />
                </div>
              </div>
            </div>
            <div class="mt-4 xl:mt-6 text-gray-800 text-sm">
              <p>Thanks so much!! Can’t wait to try it out :)</p>
            </div>
          </article>
          <article
            class="mt-3 px-6 pt-4 pb-6 xl:px-10 xl:pt-6 xl:pb-8 bg-white rounded-lg shadow"
          >
            <div class="flex items-center md:block">
              <div>
                <img
                  class="md:hidden h-9 w-8 rounded-full object-cover"
                  src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=144&q=80"
                  alt=""
                />
              </div>
              <div
                class="ml-3 md:ml-0 md:flex md:items-center md:justify-between"
              >
                <p class="text-base font-semibold leading-tight xl:text-lg">
                  <span class="text-gray-900">Monica White</span>
                  <span class="text-gray-600">wrote</span>
                </p>
                <div class="flex items-center">
                  <span class="text-sm text-gray-600">
                    Yesterday at 7:24 AM
                  </span>
                  <img
                    class="hidden md:block ml-5 h-9 w-8 rounded-full object-cover"
                    src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=144&q=80"
                    alt=""
                  />
                </div>
              </div>
            </div>
            <div class="mt-4 xl:mt-6 text-gray-800 text-sm">
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Malesuada at ultricies tincidunt elit et, enim. Habitant nunc,
                adipiscing non fermentum, sed est a, aliquet. Lorem in vel
                libero vel augue aliquet dui commodo.
              </p>
              <p class="mt-4">
                Nec malesuada sed sit ut aliquet. Cras ac pharetra, sapien
                purus vitae vestibulum auctor faucibus ullamcorper. Leo quam
                tincidunt porttitor neque, velit sed. Tortor mauris ornare ut
                tellus sed aliquet amet venenatis condimentum. Convallis
                accumsan et nunc eleifend.
              </p>
              <p class="mt-4 font-semibold text-gray-900">Monica White</p>
              <p>Customer Service</p>
            </div>
          </article>
          <article
            class="mt-3 px-6 pt-4 pb-6 xl:px-10 xl:pt-6 xl:pb-8 bg-white rounded-lg shadow"
          >
            <div class="flex items-center md:block">
              <div>
                <img
                  class="md:hidden h-9 w-8 rounded-full object-cover"
                  src="https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3.5&w=144&h=144&q=80"
                  alt=""
                />
              </div>
              <div
                class="ml-3 md:ml-0 md:flex md:items-center md:justify-between"
              >
                <p class="text-base font-semibold leading-tight xl:text-lg">
                  <span class="text-gray-900">Joe Armstrong</span>
                  <span class="text-gray-600">wrote</span>
                </p>
                <div class="flex items-center">
                  <span class="text-sm text-gray-600">
                    Yesterday at 7:24 AM
                  </span>
                  <img
                    class="hidden md:block ml-5 h-9 w-8 rounded-full object-cover"
                    src="https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3.5&w=144&h=144&q=80"
                    alt=""
                  />
                </div>
              </div>
            </div>
            <div class="mt-4 xl:mt-6 text-gray-800 text-sm">
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Malesuada at ultricies tincidunt elit et, enim. Habitant nunc,
                adipiscing non fermentum, sed est a, aliquet. Lorem in vel
                libero vel augue aliquet dui commodo.
              </p>
              <p class="mt-4">
                Nec malesuada sed sit ut aliquet. Cras ac pharetra, sapien
                purus vitae vestibulum auctor faucibus ullamcorper. Leo quam
                tincidunt porttitor neque, velit sed. Tortor mauris ornare ut
                tellus sed aliquet amet venenatis condimentum. Convallis
                accumsan et nunc eleifend.
              </p>
            </div>
          </article>
        </div>
      </div>
    </main>
  </div>
</div>

'''
ui_string = """
<div id="app" class="h-screen flex flex-col">
  <header class="flex flex-shrink-0">
    <div class="flex-shrink-0 px-4 py-3 bg-gray-700 lg:w-64 lg:bg-gray-800">
      <button
        @click="sidebarOpen = true"
        class="block text-gray-400 hover:text-gray-200 sm:hidden"
      >
        <svg class="h-6 w-6" viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M3 6a1 1 0 011-1h16a1 1 0 110 2H4a1 1 0 01-1-1zM3 12a1 1 0 011-1h16a1 1 0 110 2H4a1 1 0 01-1-1zM4 17a1 1 0 100 2h7a1 1 0 100-2H4z"
          />
        </svg>
      </button>

      <button class="hidden sm:flex sm:items-center sm:w-full">
        <img
          class="h-8 w-8 rounded-full object-cover"
          src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=144&h=144&q=80"
          alt=""
        />
        <span
          class="hidden lg:inline ml-4 mr-2 text-sm font-medium text-white"
        >
          Monica White
        </span>
        <svg
          class="ml-2 h-6 w-6 fill-current text-gray-400 lg:ml-auto"
          viewBox="0 0 24 24"
        >
          <path
            d="M7.293 9.293a1 1 0 011.414 0L12 12.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
          />
        </svg>
      </button>
    </div>
    <div
      class="flex-1 flex items-center justify-between pl-2 pr-6 bg-gray-700 lg:px-6"
    >
      <nav class="hidden sm:flex">
        <a
          href="#"
          class="inline-block px-3 py-2 bg-gray-800 rounded-lg leading-none text-sm font-medium text-white"
        >
          Mailbox
        </a>
        <a
          href="#"
          class="ml-2 inline-block px-3 py-2 rounded-lg leading-none text-sm font-medium text-white hover:bg-gray-600"
        >
          Customers
        </a>
        <a
          href="#"
          class="ml-2 inline-block px-3 py-2 rounded-lg leading-none text-sm font-medium text-white hover:bg-gray-600"
        >
          Reporting
        </a>
        <a
          href="#"
          class="ml-2 inline-block px-3 py-2 rounded-lg leading-none text-sm font-medium text-white hover:bg-gray-600"
        >
          Manage
        </a>
      </nav>
      <div class="ml-auto flex items-center">
        <button class="lg:hidden ml-5 text-gray-400 hover:text-gray-200">
          <svg class="h-5 w-5 fill-current" viewBox="0 0 24 24">
            <path
              d="M10 4a6 6 0 100 12 6 6 0 000-12zm-8 6a8 8 0 1114.32 4.906l5.387 5.387a1 1 0 01-1.414 1.414l-5.387-5.387A8 8 0 012 10z"
            />
          </svg>
        </button>
        <div class="hidden lg:block relative w-64">
          <span class="absolute inset-y-0 left-0 flex items-center pl-2">
            <svg
              class="h-5 w-5 fill-current text-gray-500"
              viewBox="0 0 24 24"
            >
              <path
                d="M10 4a6 6 0 100 12 6 6 0 000-12zm-8 6a8 8 0 1114.32 4.906l5.387 5.387a1 1 0 01-1.414 1.414l-5.387-5.387A8 8 0 012 10z"
              />
            </svg>
          </span>
          <input
            class="block pl-9 pr-4 py-2 w-full bg-gray-800 rounded-lg text-sm placeholder-gray-400 text-white focus:bg-white focus:placeholder-gray-600 focus:text-gray-900 focus:outline-none"
            placeholder="Search"
          />
        </div>
        <button class="ml-5 text-gray-400 hover:text-gray-200">
          <svg class="h-5 w-5 fill-current" viewBox="0 0 24 24">
            <path
              d="M9.018 4.665a3 3 0 015.964 0A7 7 0 0119 11v3.159c0 .273.109.535.302.729l1.405 1.405A1 1 0 0120 18H4a1 1 0 01-.707-1.707l1.405-1.405c.193-.194.302-.456.302-.73V11a7 7 0 014.018-6.335zM12 4a1 1 0 00-1 1v1.049l-.667.235A5.002 5.002 0 007 11v3.159c0 .669-.221 1.315-.623 1.841h11.246A3.032 3.032 0 0117 14.159V11a5.002 5.002 0 00-3.333-4.716L13 6.05V5a1 1 0 00-1-1zM10 18a2 2 0 004 0h2a4 4 0 11-8 0h2z"
            />
          </svg>
        </button>
        <button class="ml-4 text-gray-400 hover:text-gray-200">
          <svg class="h-5 w-5 fill-current" viewBox="0 0 24 24">
            <path d="M12 18a1 1 0 100-2 1 1 0 000 2z" />
            <path
              d="M12 4a8 8 0 100 16 8 8 0 000-16zM2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12z"
            />
            <path
              d="M12 8c-1.472 0-2.528.706-2.868 1.426a1 1 0 01-1.809-.852C8.082 6.964 9.99 6 12 6c1.3 0 2.515.394 3.428 1.079C16.343 7.764 17 8.786 17 10c0 2.07-1.834 3.508-3.817 3.889a.31.31 0 00-.162.083A.107.107 0 0013 14a1 1 0 01-2 0c0-1.142.909-1.904 1.805-2.075C14.279 11.642 15 10.729 15 10c0-.443-.237-.92-.771-1.321C13.694 8.278 12.909 8 12 8z"
            />
          </svg>
        </button>
      </div>
    </div>
  </header>
  <div class="flex-1 flex overflow-hidden">
    <div
      class="z-30 fixed inset-y-0 left-0 w-64 bg-gray-100 border-r overflow-y-auto sm:static sm:block sm:translate-x-0 sm:transition-none"
    >
      <div class="absolute top-0 left-0 pl-4 pt-3 sm:hidden">
        <button
          @click="sidebarOpen = false"
          class="block text-gray-600 hover:text-gray-800"
        >
          <svg class="h-6 w-6" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M17.293 18.707a1 1 0 001.414-1.414L13.414 12l5.293-5.293a1 1 0 00-1.414-1.414L12 10.586 6.707 5.293a1 1 0 00-1.414 1.414L10.586 12l-5.293 5.293a1 1 0 101.414 1.414L12 13.414l5.293 5.293z"
            />
          </svg>
        </button>
      </div>
      <nav class="mt-16 sm:mt-0">
        <div class="px-6 sm:hidden">
          <a href="#" class="block py-1  text-sm font-medium text-gray-900">
            Mailbox
          </a>
          <a
            href="#"
            class="mt-2 block py-1  text-sm font-medium text-gray-900"
          >
            Customers
          </a>
          <a
            href="#"
            class="mt-2 block py-1  text-sm font-medium text-gray-900"
          >
            Reporting
          </a>
          <a
            href="#"
            class="mt-2 block py-1  text-sm font-medium text-gray-900"
          >
            Manage
          </a>
        </div>
        <div class="mt-8 px-6">
          <h2
            class="text-xs font-semibold text-gray-600 uppercase tracking-wide"
          >
            Mailboxes
          </h2>
          <div class="mt-3">
            <a
              href="#"
              class="-mx-3 px-3 py-2 flex items-center justify-between text-sm font-medium bg-gray-200 rounded-lg"
            >
              <span class="inline-flex">
                <svg
                  class="h-6 w-6 fill-current text-gray-700"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M3 6a3 3 0 013-3h12a3 3 0 013 3v12a3 3 0 01-3 3H6a3 3 0 01-3-3V6zm3-1a1 1 0 00-1 1v6h1.586A2 2 0 018 12.586L10.414 15h3.172L16 12.586A2 2 0 0117.414 12H19V6a1 1 0 00-1-1H6zm13 9h-1.586L15 16.414a2 2 0 01-1.414.586h-3.172A2 2 0 019 16.414L6.586 14H5v4a1 1 0 001 1h12a1 1 0 001-1v-4z"
                  />
                </svg>
                <span class="ml-2 text-gray-900">Inbox</span>
              </span>
              <span
                class="inline-block w-9 text-center py-1 leading-none text-xs font-semibold text-gray-700 bg-gray-300 rounded-full"
              >
                6
              </span>
            </a>
            <a
              href="#"
              class="mt-2 -mx-3 px-3 py-2 flex items-center justify-between text-sm font-medium hover:bg-gray-200 rounded-lg"
            >
              <span class="inline-flex">
                <svg
                  class="h-6 w-6 fill-current text-gray-500"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M5 4a1 1 0 00-1 1v9.17c.313-.11.65-.17 1-.17h6.5a1 1 0 01.707.293l.707.707h6.468l-2.276-4.553a1 1 0 010-.894L19.382 5H13v4a1 1 0 11-2 0V4H5zm7.914-1H21a1 1 0 01.894 1.447L19.118 10l2.776 5.553A1 1 0 0121 17h-8.5a1 1 0 01-.707-.293L11.086 16H5a1 1 0 00-1 1v4a1 1 0 11-2 0V5a3 3 0 013-3h6.5a1 1 0 01.707.293l.707.707z"
                  />
                </svg>
                <span class="ml-2 text-gray-700">Flagged</span>
              </span>
            </a>
            <a
              href="#"
              class="mt-2 -mx-3 px-3 py-2 flex items-center justify-between text-sm font-medium hover:bg-gray-200 rounded-lg"
            >
              <span class="inline-flex">
                <svg
                  class="h-6 w-6 fill-current text-gray-500"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M19.707 4.293a1 1 0 00-1.414 0L10 12.586V14h1.414l8.293-8.293a1 1 0 000-1.414zM16.88 2.879A3 3 0 1121.12 7.12l-8.585 8.586a1 1 0 01-.708.293H9a1 1 0 01-1-1v-2.828a1 1 0 01.293-.708l8.586-8.585zM6 6a1 1 0 00-1 1v11a1 1 0 001 1h11a1 1 0 001-1v-5a1 1 0 112 0v5a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h5a1 1 0 110 2H6z"
                  />
                </svg>
                <span class="ml-2 text-gray-700">Drafts</span>
              </span>
              <span
                class="inline-block w-9 text-center py-1 leading-none text-xs font-semibold text-gray-700 bg-gray-300 rounded-full"
              >
                2
              </span>
            </a>
            <a
              href="#"
              class="mt-2 -mx-3 px-3 py-2 flex items-center justify-between text-sm font-medium hover:bg-gray-200 rounded-lg"
            >
              <span class="inline-flex">
                <svg
                  class="h-6 w-6 fill-current text-gray-500"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M12 4a8 8 0 00-6.598 12.526A14.943 14.943 0 0112 15c2.366 0 4.606.548 6.598 1.526A8 8 0 0012 4zm5.199 14.08A12.954 12.954 0 0012 17c-1.85 0-3.607.386-5.199 1.08A7.968 7.968 0 0012 20c1.985 0 3.8-.723 5.199-1.92zM2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12zm10-4a2 2 0 100 4 2 2 0 000-4zm-4 2a4 4 0 118 0 4 4 0 01-8 0z"
                  />
                </svg>
                <span class="ml-2 text-gray-700">Assigned</span>
              </span>
              <span
                class="inline-block w-9 text-center py-1 leading-none text-xs font-semibold text-gray-700 bg-gray-300 rounded-full"
              >
                1
              </span>
            </a>
            <a
              href="#"
              class="mt-2 -mx-3 px-3 py-2 flex items-center justify-between text-sm font-medium hover:bg-gray-200 rounded-lg"
            >
              <span class="inline-flex">
                <svg
                  class="h-6 w-6 fill-current text-gray-500"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M12 4a8 8 0 100 16 8 8 0 000-16zM2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12zm13.707-2.707a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-2-2a1 1 0 111.414-1.414L11 12.586l3.293-3.293a1 1 0 011.414 0z"
                  />
                </svg>
                <span class="ml-2 text-gray-700">Closed</span>
              </span>
            </a>
            <a
              href="#"
              class="mt-2 -mx-3 px-3 py-2 flex items-center justify-between text-sm font-medium hover:bg-gray-200 rounded-lg"
            >
              <span class="inline-flex">
                <svg
                  class="h-6 w-6 fill-current text-gray-500"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M2 6a3 3 0 013-3h14a3 3 0 011 5.83V18a3 3 0 01-3 3H7a3 3 0 01-3-3V8.83A3.001 3.001 0 012 6zm4 3v9a1 1 0 001 1h10a1 1 0 001-1V9H6zM5 5a1 1 0 000 2h14a1 1 0 100-2H5zm4 7a1 1 0 011-1h4a1 1 0 110 2h-4a1 1 0 01-1-1z"
                  />
                </svg>
                <span class="ml-2 text-gray-700">Junk</span>
              </span>
            </a>
          </div>
          <h2
            class="mt-8 text-xs font-semibold text-gray-600 uppercase tracking-wide"
          >
            Folders
          </h2>
          <div class="mt-4">
            <a href="#" class="block text-sm font-medium text-gray-700">
              Refunds
            </a>
            <a href="#" class="mt-4 block text-sm font-medium text-gray-700">
              Discounts
            </a>
            <a href="#" class="mt-4 block text-sm font-medium text-gray-700">
              Bugs
            </a>
          </div>
        </div>
        <div class="mt-8 p-6 border-t sm:hidden">
          <div class="flex items-center">
            <img
              class="h-8 w-8 rounded-full object-cover"
              src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=144&h=144&q=80"
              alt=""
            />
            <span class="ml-4 mr-2 text-sm font-medium text-gray-800">
              Monica White
            </span>
          </div>
          <div class="mt-4">
            <a href="#" class="block text-sm font-medium text-gray-700">
              Settings
            </a>
            <a href="#" class="mt-4 block text-sm font-medium text-gray-700">
              Log out
            </a>
          </div>
        </div>
      </nav>
    </div>
    <main class="flex-1 flex bg-gray-200">
      <div
        class="hidden lg:flex flex-col relative z-10 w-full max-w-xs flex-grow flex-shrink-0 border-r bg-gray-300"
      >
        <div
          class="flex-shrink-0 px-4 py-2 flex items-center justify-between border-b bg-gray-200"
        >
          <button
            class="flex items-center text-xs font-semibold text-gray-600"
          >
            Sorted by Date
            <svg
              class="ml-1 h-6 w-6 fill-current text-gray-500"
              viewBox="0 0 24 24"
            >
              <path
                d="M7.293 9.293a1 1 0 011.414 0L12 12.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
              />
            </svg>
          </button>
          <button>
            <svg
              class="h-6 w-6 fill-current text-gray-500"
              viewBox="0 0 24 24"
            >
              <path
                d="M16 3H3a1 1 0 000 2h13a1 1 0 100-2zm-4 4H3a1 1 0 000 2h9a1 1 0 100-2zm-9 4h6a1 1 0 110 2H3a1 1 0 110-2zm9.293.293l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L18 10.414V20a1 1 0 11-2 0v-9.586l-2.293 2.293a1 1 0 01-1.414-1.414z"
              />
            </svg>
          </button>
        </div>
        <div class="flex-1 overflow-y-auto">
          <div class="shadow">
            <div>
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-indigo-100 border-l-4 border-indigo-500"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Joe Armstrong
                  </span>
                  <span class="text-sm text-gray-600">
                    1 day ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Re: Student Discount?
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Gloria Roberston
                  </span>
                  <span class="text-sm text-gray-600">
                    2 days ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Refund
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Pat Steward
                  </span>
                  <span class="text-sm text-gray-600">
                    4 days ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Issue with reporting
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Jerome Warren
                  </span>
                  <span class="text-sm text-gray-600">
                    4 days ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Email not working
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Gladys Mccoy
                  </span>
                  <span class="text-sm text-gray-600">
                    4 days ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Do you have a student discount?
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Jorge Murphy
                  </span>
                  <span class="text-sm text-gray-600">
                    1 week ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Not what I expected
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Paxton Walter
                  </span>
                  <span class="text-sm text-gray-600">
                    1 week ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  SEO opportunity
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
            <div class="border-t">
              <a
                href="#"
                class="block px-6 pt-3 pb-4 bg-white border-l-4 border-transparent hover:bg-gray-100"
              >
                <div class="flex justify-between">
                  <span class="text-sm font-semibold text-gray-900">
                    Kristopher Donnelly
                  </span>
                  <span class="text-sm text-gray-600">
                    2 weeks ago
                  </span>
                </div>
                <p class="text-sm text-gray-900">
                  Don't know where to start
                </p>
                <p class="mt-1 text-sm text-gray-600">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Nunc tempus element...
                </p>
              </a>
            </div>
          </div>
        </div>
      </div>
      <div class="flex-1 flex flex-col w-0 overflow-hidden">
        <div class="relative shadow-md">
          <div
            class="flex items-center justify-between px-5 py-4 bg-gray-100 border-b"
          >
            <div class="flex items-center">
              <button>
                <svg
                  class="h-6 w-6 fill-current text-gray-600"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M9.707 3.293a1 1 0 010 1.414L5.414 9H13a9 9 0 019 9v2a1 1 0 11-2 0v-2a7 7 0 00-7-7H5.414l4.293 4.293a1 1 0 01-1.414 1.414l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 0z"
                  />
                </svg>
              </button>
              <button class="ml-6">
                <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none">
                  <circle
                    class="fill-current text-gray-600"
                    cx="7"
                    cy="7"
                    r="1"
                  />
                  <path
                    class="stroke-current text-gray-600"
                    d="M12 3H7a4 4 0 00-4 4v5c0 .512.195 1.024.586 1.414l7 7a2 2 0 002.828 0l7-7a2 2 0 000-2.828l-7-7A1.993 1.993 0 0012 3z"
                    stroke-width="2"
                  />
                </svg>
              </button>
              <button class="ml-6">
                <svg
                  class="h-6 w-6 fill-current text-gray-600"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M12 4a8 8 0 00-6.598 12.526A14.943 14.943 0 0112 15c2.366 0 4.606.548 6.598 1.526A8 8 0 0012 4zm5.199 14.08A12.954 12.954 0 0012 17c-1.85 0-3.607.386-5.199 1.08A7.968 7.968 0 0012 20c1.985 0 3.8-.723 5.199-1.92zM2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12zm10-4a2 2 0 100 4 2 2 0 000-4zm-4 2a4 4 0 118 0 4 4 0 01-8 0z"
                  />
                </svg>
              </button>
              <button class="ml-6">
                <svg
                  class="h-6 w-6 fill-current text-gray-600"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M5 6a1 1 0 00-1 1v10a1 1 0 001 1h14a1 1 0 001-1V9a1 1 0 00-1-1h-6.414l-2-2H5zM2 7a3 3 0 013-3h6.414l2 2H19a3 3 0 013 3v8a3 3 0 01-3 3H5a3 3 0 01-3-3V7zm10 2a1 1 0 011 1v3.586l1.293-1.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 111.414-1.414L11 13.586V10a1 1 0 011-1z"
                  />
                </svg>
              </button>
              <button class="ml-6">
                <svg
                  class="h-6 w-6 fill-current text-gray-600"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M7 12a2 2 0 11-4 0 2 2 0 014 0zm7 0a2 2 0 11-4 0 2 2 0 014 0zm5 2a2 2 0 100-4 2 2 0 000 4z"
                  />
                </svg>
              </button>
            </div>
            <div class="flex items-center">
              <button>
                <svg
                  class="h-6 w-6 text-gray-600"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  fill="none"
                >
                  <path
                    d="M19 9l-7 7-7-7"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </button>
              <button class="ml-2">
                <svg
                  class="h-6 w-6 text-gray-600"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                >
                  <path
                    d="M5 16l7-7 7 7"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </button>
            </div>
          </div>
          <div class="flex items-center justify-between px-5 py-4 bg-white">
            <h3
              class="text-base lg:text-lg xl:text-xl text-gray-900 truncate"
            >
              Re: Student discount?
            </h3>
            <div class="ml-4 flex-shrink-0">
              <span class="text-sm lg:text-base">#1428</span>
              <span
                class="ml-2 text-xs font-semibold text-green-900 bg-green-200 rounded-full leading-none px-2 py-1 lg:text-sm"
                >Active</span
              >
            </div>
          </div>
        </div>
        <div class="p-3 flex-1 overflow-y-auto">
          <article
            class="px-6 pt-4 pb-6 xl:px-10 xl:pt-6 xl:pb-8 bg-white rounded-lg shadow"
          >
            <div class="flex items-center md:block">
              <div>
                <img
                  class="md:hidden h-9 w-9 rounded-full object-cover"
                  src="https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3.5&w=144&h=144&q=80"
                  alt=""
                />
              </div>
              <div
                class="ml-3 md:ml-0 md:flex md:items-center md:justify-between"
              >
                <p class="text-base font-semibold leading-tight xl:text-lg">
                  <span class="text-gray-900">Joe Armstrong</span>
                  <span class="text-gray-600">wrote</span>
                </p>
                <div class="flex items-center">
                  <span class="text-sm text-gray-600">
                    Yesterday at 7:24 AM
                  </span>
                  <img
                    class="hidden md:block ml-5 h-9 w-9 rounded-full object-cover"
                    src="https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3.5&w=144&h=144&q=80"
                    alt=""
                  />
                </div>
              </div>
            </div>
            <div class="mt-4 xl:mt-6 text-gray-800 text-sm">
              <p>Thanks so much!! Can’t wait to try it out :)</p>
            </div>
          </article>
          <article
            class="mt-3 px-6 pt-4 pb-6 xl:px-10 xl:pt-6 xl:pb-8 bg-white rounded-lg shadow"
          >
            <div class="flex items-center md:block">
              <div>
                <img
                  class="md:hidden h-9 w-9 rounded-full object-cover"
                  src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=144&q=80"
                  alt=""
                />
              </div>
              <div
                class="ml-3 md:ml-0 md:flex md:items-center md:justify-between"
              >
                <p class="text-base font-semibold leading-tight xl:text-lg">
                  <span class="text-gray-900">Monica White</span>
                  <span class="text-gray-600">wrote</span>
                </p>
                <div class="flex items-center">
                  <span class="text-sm text-gray-600">
                    Yesterday at 7:24 AM
                  </span>
                  <img
                    class="hidden md:block ml-5 h-9 w-9 rounded-full object-cover"
                    src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=144&q=80"
                    alt=""
                  />
                </div>
              </div>
            </div>
            <div class="mt-4 xl:mt-6 text-gray-800 text-sm">
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Malesuada at ultricies tincidunt elit et, enim. Habitant nunc,
                adipiscing non fermentum, sed est a, aliquet. Lorem in vel
                libero vel augue aliquet dui commodo.
              </p>
              <p class="mt-4">
                Nec malesuada sed sit ut aliquet. Cras ac pharetra, sapien
                purus vitae vestibulum auctor faucibus ullamcorper. Leo quam
                tincidunt porttitor neque, velit sed. Tortor mauris ornare ut
                tellus sed aliquet amet venenatis condimentum. Convallis
                accumsan et nunc eleifend.
              </p>
              <p class="mt-4 font-semibold text-gray-900">Monica White</p>
              <p>Customer Service</p>
            </div>
          </article>
          <article
            class="mt-3 px-6 pt-4 pb-6 xl:px-10 xl:pt-6 xl:pb-8 bg-white rounded-lg shadow"
          >
            <div class="flex items-center md:block">
              <div>
                <img
                  class="md:hidden h-9 w-9 rounded-full object-cover"
                  src="https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3.5&w=144&h=144&q=80"
                  alt=""
                />
              </div>
              <div
                class="ml-3 md:ml-0 md:flex md:items-center md:justify-between"
              >
                <p class="text-base font-semibold leading-tight xl:text-lg">
                  <span class="text-gray-900">Joe Armstrong</span>
                  <span class="text-gray-600">wrote</span>
                </p>
                <div class="flex items-center">
                  <span class="text-sm text-gray-600">
                    Yesterday at 7:24 AM
                  </span>
                  <img
                    class="hidden md:block ml-5 h-9 w-9 rounded-full object-cover"
                    src="https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3.5&w=144&h=144&q=80"
                    alt=""
                  />
                </div>
              </div>
            </div>
            <div class="mt-4 xl:mt-6 text-gray-800 text-sm">
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Malesuada at ultricies tincidunt elit et, enim. Habitant nunc,
                adipiscing non fermentum, sed est a, aliquet. Lorem in vel
                libero vel augue aliquet dui commodo.
              </p>
              <p class="mt-4">
                Nec malesuada sed sit ut aliquet. Cras ac pharetra, sapien
                purus vitae vestibulum auctor faucibus ullamcorper. Leo quam
                tincidunt porttitor neque, velit sed. Tortor mauris ornare ut
                tellus sed aliquet amet venenatis condimentum. Convallis
                accumsan et nunc eleifend.
              </p>
            </div>
          </article>
        </div>
      </div>
    </main>
  </div>
</div>
"""

def ui_test():
    wp = jp.WebPage()
    wp.css = """
    .w-9 {width: 2.25rem;)
    """
    wp.body_classes = 'antialiased font-sans bg-gray-200'
    jp.parse_html(ui_string, a=wp)
    return wp

jp.justpy(ui_test)