console.info(`============================HOST_IP:${process.env.NEXT_HOST_IP}===========================`)
export const HOST_IP=process.env.NEXT_HOST_IP||'api-gateway'
export const PUBLIC_URL=`http://0.0.0.0:3000/`
export const PRODUCT_IMAGE_URLS=`http://${HOST_IP}:80/`

