/* ================================================
   Audio Module
   Om Chant via YouTube IFrame Player API
   Plays the real Om chanting audio from YouTube
   Video: https://youtube.com/watch?v=xIJQ-68zgnY
   ================================================ */

const Audio = (() => {
    const VIDEO_ID = 'xIJQ-68zgnY';
    let player = null;
    let isReady = false;
    let isPlaying = false;
    let currentVolume = 15; // 0-100 scale, starts low
    let pendingPlay = false;

    // Load YouTube IFrame API script
    function loadAPI() {
        if (document.getElementById('yt-api-script')) return;
        const tag = document.createElement('script');
        tag.id = 'yt-api-script';
        tag.src = 'https://www.youtube.com/iframe_api';
        document.head.appendChild(tag);
    }

    // Called automatically by the YouTube API when it's ready
    function createPlayer() {
        player = new YT.Player('yt-om-player', {
            videoId: VIDEO_ID,
            playerVars: {
                autoplay: 0,
                loop: 1,
                playlist: VIDEO_ID, // Required for loop to work
                controls: 0,
                disablekb: 1,
                fs: 0,
                modestbranding: 1,
                rel: 0,
                showinfo: 0,
                iv_load_policy: 3, // No annotations
            },
            events: {
                onReady: onPlayerReady,
                onStateChange: onPlayerStateChange,
                onError: onPlayerError
            }
        });
    }

    function onPlayerReady() {
        isReady = true;
        player.setVolume(currentVolume);

        // If startOm was called before the player was ready
        if (pendingPlay) {
            pendingPlay = false;
            doPlay();
        }
    }

    function onPlayerStateChange(event) {
        // YT.PlayerState.ENDED = 0 — restart for seamless loop
        if (event.data === 0 && isPlaying) {
            player.seekTo(0);
            player.playVideo();
        }
    }

    function onPlayerError(event) {
        console.warn('YouTube Om player error:', event.data);
        // Silently fail — audio is a nice-to-have, not critical
    }

    function doPlay() {
        if (!player || !isReady) return;
        player.setVolume(currentVolume);
        player.seekTo(0);
        player.playVideo();
        isPlaying = true;
    }

    // === Public API ===

    function startOm() {
        if (isPlaying) return;

        if (!isReady) {
            // Player not ready yet — queue the play
            pendingPlay = true;
            return;
        }

        doPlay();
    }

    function stopOm() {
        if (!isPlaying) return;

        if (player && isReady) {
            // Fade out by stepping volume down
            const startVol = player.getVolume();
            let vol = startVol;
            const fadeInterval = setInterval(() => {
                vol -= 2;
                if (vol <= 0) {
                    clearInterval(fadeInterval);
                    player.pauseVideo();
                    player.setVolume(currentVolume); // Restore for next time
                    isPlaying = false;
                } else {
                    player.setVolume(vol);
                }
            }, 50); // ~2 second fade out (100 steps / 2 per step @ 50ms)
        }

        isPlaying = false;
    }

    function setVolume(vol) {
        // vol comes in 0-1 from slider, convert to 0-100
        currentVolume = Math.round(Math.max(0, Math.min(1, vol)) * 100);
        if (player && isReady && isPlaying) {
            player.setVolume(currentVolume);
        }
    }

    function getVolume() {
        return currentVolume / 100;
    }

    function getIsPlaying() {
        return isPlaying;
    }

    // Initialize: load the API immediately
    loadAPI();

    return { startOm, stopOm, setVolume, getVolume, getIsPlaying, createPlayer };
})();

// YouTube API calls this global function when it's loaded
function onYouTubeIframeAPIReady() {
    Audio.createPlayer();
}
