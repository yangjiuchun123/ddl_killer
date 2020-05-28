import { JSEncrypt } from 'jsencrypt'
import { getPubKey } from '@/api/user'

const pub_key = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCt1/hVqW9pxTAp6vbJu5+5myvA\nF8wvsEqM7FdIAKe5hhD1paQhPcG/RkPFzQG1u0jeQcwNJIddhmk/jqAK0v2GbHhV\nUEw/rQ8AATFxLTitXWhjFPC2quAlGRzRby4LALxlWBziGNzKU6BERsI1nawJb1If\ni/+q/qgZMCAGKY1EAwIDAQAB\n-----END PUBLIC KEY-----'

export async function encrypt(password) {
    var encPass = ""
    console.log("get in encrypt")
    await getPubKey().then(res => {
        // console.log(res)
        let enc = new JSEncrypt()
        // res : {'pub_key': pub_key, 'key_id': key.id}
        // console.log("res.key_id: ", res.key_id)
        // console.log("pub_key: ", res.pub_key)
        enc.setPublicKey(res.pub_key)
        encPass = "kid:" + res.key_id + "|" + enc.encrypt(password)
    })
    return encPass
    
}

// export function encrypt(password) {
//     let enc = new JSEncrypt()
//     enc.setPublicKey(pub_key)
//     return enc.encrypt(password)
// }