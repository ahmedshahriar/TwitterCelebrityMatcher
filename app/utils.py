def social_share_msg(user1, user2, score) -> str:
    """
    :return: social media share message
    """

    # st.markdown('<svg width="24px" height="24px" enable-background="new 0 0 512 512" version="1.1"
    # viewBox="0 0 512 512" xml:space="preserve" xmlns="http://www.w3.org/2000/svg"><path d="m509.01
    # 206.16-176.92-176.92c-2.917-2.917-7.304-3.789-11.115-2.21-3.81 1.579-6.296 5.299-6.296
    # 9.423v96.287h-49.705c-70.777 0-137.32 27.562-187.36 77.609s-77.609 116.59-77.609 187.36v77.833c0
    # 4.209 2.586 7.986 6.51 9.509 1.199 0.466 2.449 0.691 3.687 0.691 2.81 0 5.561-1.163
    # 7.531-3.32l92.966-101.74c50.333-55.084 122-86.677 196.61-86.677h7.374v96.288c0 4.126 2.486 7.844
    # 6.296 9.423 3.811 1.581 8.198 0.706 11.115-2.21l176.92-176.92c1.912-1.912 2.987-4.507
    # 2.987-7.212s-1.075-5.299-2.987-7.211zm-173.94
    # 159.51v-81.864c0-5.633-4.567-10.199-10.199-10.199h-17.573c-80.331 0-157.48 34.012-211.67
    # 93.316l-75.237 82.339v-51.551c0-134.86 109.72-244.58 244.58-244.58h59.904c5.632 0 10.199-4.566
    # 10.199-10.199v-81.864l152.3 152.3-152.3 152.3z"/><path d="m255.45 170.33c-2.779 0-5.588 0.057-8.35
    # 0.168-5.628 0.226-10.008 4.973-9.78 10.601 0.221 5.489 4.74 9.789 10.184 9.789 0.139 0 0.278-2e-3
    # 0.417-9e-3 2.49-0.1 5.022-0.151 7.529-0.151 5.633 0 10.199-4.566
    # 10.199-10.199s-4.566-10.199-10.199-10.199z"/><path d="m221.1
    # 183.28c-1.279-5.485-6.759-8.895-12.249-7.616-26.861 6.264-51.802 17.74-74.131 34.11-4.544
    # 3.33-5.526 9.713-2.196 14.255 1.998 2.725 5.094 4.169 8.234 4.169 2.093 0 4.205-0.641 6.023-1.975
    # 20.096-14.733 42.54-25.06 66.704-30.696 5.485-1.277 8.894-6.761 7.615-12.247z"/></svg>',
    # unsafe_allow_html=True)

    return f"""
    Share the result on - <span><a href="https://twitter.com/intent/tweet?hashtags=streamlit%2Cpython
    &amp;text=The%20similarity%20score%20between%20@{user1}%20and%20@{user2}%20
    is%20{score * 100:.3f}%25%21%20Check%20this%20app%20to%20compare%20twitter%20users%0A&amp;
    url=https%3A%2F%2Fshare.streamlit.io%2Fahmedshahriar%2Ftwittercelebritymatcher%2Fmain%2Fmain.py%0A" 
    target="_blank" rel="noopener noreferrer"><svg width="36" height="36" viewBox="0 0 48 48" fill="none" 
    xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="24" r="24" fill="#56CCF2"></circle><path 
    d="M35 15.0003C34.0424 15.6758 32.9821 16.1924 31.86 16.5303C31.2577 15.8378 30.4573 15.347 29.567 
    15.1242C28.6767 14.9015 27.7395 14.9575 26.8821 15.2847C26.0247 15.612 25.2884 16.1947 24.773 
    16.954C24.2575 17.7133 23.9877 18.6126 24 19.5303V20.5303C22.2426 20.5759 20.5013 20.1861 18.931 
    19.3957C17.3607 18.6054 16.0103 17.4389 15 16.0003C15 16.0003 11 25.0003 20 29.0003C17.9405 30.3983 
    15.4872 31.0992 13 31.0003C22 36.0003 33 31.0003 33 19.5003C32.9991 19.2217 32.9723 18.9439 32.92 
    18.6703C33.9406 17.6638 34.6608 16.393 35 15.0003Z" fill="white"></path></svg></a>   <a 
    href="https://www.linkedin.com/sharing/share-offsite/?summary=https%3A%2F%2Fshare.streamlit.io
    %2Fahmedshahriar%2Ftwittercelebritymatcher%2Fmain%2Fmain.py%20%23streamlit%20%23python&amp;title
    =Check%20out%20this%20awesome%20Streamlit%20app%20I%20built%0A&amp;url=https%3A%2F%2Fshare.streamlit
    .io%2Fahmedshahriar%2Ftwittercelebritymatcher%2Fmain%2Fmain.py" target="_blank" rel="noopener 
    noreferrer"><svg width="36" height="36" viewBox="0 0 48 48" fill="none" 
    xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="24" r="24" fill="#1C83E1"></circle><path 
    d="M28 20C29.5913 20 31.1174 20.6321 32.2426 21.7574C33.3679 22.8826 34 24.4087 34 26V33H30V26C30 
    25.4696 29.7893 24.9609 29.4142 24.5858C29.0391 24.2107 28.5304 24 28 24C27.4696 24 26.9609 24.2107 
    26.5858 24.5858C26.2107 24.9609 26 25.4696 26 26V33H22V26C22 24.4087 22.6321 22.8826 23.7574 
    21.7574C24.8826 20.6321 26.4087 20 28 20Z" fill="white"></path><path d="M18 21H14V33H18V21Z" 
    fill="white"></path><path d="M16 18C17.1046 18 18 17.1046 18 16C18 14.8954 17.1046 14 16 14C14.8954 
    14 14 14.8954 14 16C14 17.1046 14.8954 18 16 18Z" fill="white"></path></svg></a></span> """
