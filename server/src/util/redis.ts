import {createClient, RedisClientType} from "redis";
import {createHash, randomBytes} from "crypto";

namespace Redis {

    let client: RedisClientType;

    /**
     * This sets up the redis client
     * @param url The URL to connect to
     * @param password The password
     */
    export async function setup(url: string, password: string) {
        client = createClient({
            url: url,
            password: password,
        });
        await client.connect();
    }

    /**
     * This creates an access token, stores it as a key in redis (value being the user id) and returns it
     * @param user_id The user id
     * @return The access token
     */
    export async function createAccessToken(user_id: string): Promise<string> {
        const salt_and_peppered = randomBytes(16).toString('utf-8') + user_id + randomBytes(16).toString('utf-8');
        const access_token = createHash('sha512')
            .update(salt_and_peppered)
            .digest('hex');
        await client.set(access_token, user_id);
        return access_token;
    }

    /**
     * This gets the user-id attached to the access token, or 'null' if no such access token exists
     * @param access_token The access token
     * @return The user id, if the access token exists or 'null' if it doesn't
     */
    export async function getUserId(access_token: string): Promise<string | null> {
        return await client.get(access_token);
    }

}

export default Redis;
