const URLS = {
    'zod': (username: string) => `/zod/${username}/`,
    'qux': (username: string) => `/qux/${username}/`,
    'baz': (bar: string) => `/baz/${bar}/`,
    'foo': (bar: number) => `/foo/${bar}/`,
};
export default URLS;
